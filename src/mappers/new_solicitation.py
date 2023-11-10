from fastapi import APIRouter, Depends, Response, status
from ..solicitations.models import SolicitationModel, SolicitationQueueModel, SolicitationTypeEnum
from ..util.autorizations import verify_key_and_user
from ..attendants.models import AttendantRoleEnum
from ..attendants.talker import read_attendants
from decouple import config

import json

from ..util.queue import Queue

solicitations_route = APIRouter()


@solicitations_route.post("/solicitation/")
def create_new_solicitation(solicitation: SolicitationQueueModel, key: tuple = Depends(verify_key_and_user)):
    types_solicitation = [solicitation.value for solicitation in SolicitationTypeEnum]
    if solicitation.solicitation_type not in types_solicitation:
        solicitation.solicitation_type = SolicitationTypeEnum.outros.value
    queue = Queue()
    queue.send_to_queue(message=json.dumps(solicitation.__dict__, ensure_ascii=False).encode('utf-8'), queue_name=solicitation.solicitation_type)
    queue.connection.close()

    key = {'API_USER':config('API_USER'), 'API_PASSWORD': config('API_PASSWORD')}
    attendants = read_attendants(key=key)

    return Response(content=f"The solicitation has send to queue", status_code=status.HTTP_200_OK)


def get_next_message(queue_name:AttendantRoleEnum) -> SolicitationModel:
    queue = Queue()
    solicitation = json.loads(queue.consume_next_message(queue_name=queue_name)["message"])
    queue.connection.close()
    return solicitation

