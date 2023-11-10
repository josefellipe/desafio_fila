import pika
from decouple import config
from enum import Enum

class QueueName(Enum):
    cartoes = "Problemas com cartão"
    emprestimos = "Contratação de empréstimo"
    outros = "Outros Assuntos"

class Queue:
    def __init__(self):
        self.RABBITMQ_HOST = config('RABBITMQ_HOST')
        self.RABBITMQ_PORT = config('RABBITMQ_PORT')
        self.RABBITMQ_USER = config('RABBITMQ_USER')
        self.RABBITMQ_PASSWORD = config('RABBITMQ_PASSWORD')
        self.connection = self._get_connection()

    def _get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=self.RABBITMQ_HOST, port=self.RABBITMQ_PORT, credentials=pika.PlainCredentials(self.RABBITMQ_USER, self.RABBITMQ_PASSWORD)))

    def send_to_queue(self, message:str, queue_name:QueueName):
        try:
            channel = self.connection.channel()
            channel.queue_declare(queue=queue_name)
            channel.basic_publish(exchange='', routing_key=queue_name, body=message)
            return {"message": f"Item '{message}' adicionado à fila '{queue_name}' com sucesso!"}
        except Exception as e:
            return {"error": f"Erro ao adicionar item à fila '{queue_name}': {str(e)}"}

    def consume_next_message(self, queue_name:QueueName):
        try:
            channel = self.connection.channel()
            channel.queue_declare(queue=queue_name)

            method_frame, _, body = channel.basic_get(queue=queue_name)

            if method_frame:
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                return {"message": body.decode('utf-8')}
            else:
                return {"message": "Nenhuma mensagem na fila."}
        except Exception as error:
            return {"error": f"Erro ao consumir a próxima mensagem da fila '{queue_name}': {error}"}

    def get_queue_size(self, queue_name:QueueName):
        try:
            channel = self.connection.channel()
            queue_info = channel.queue_declare(queue=queue_name, passive=True)
            message_count = queue_info.method.message_count
            return message_count
        except Exception as error:
            return {"error": f"Erro ao verificar o tamanho da fila '{queue_name}': {error}"}
