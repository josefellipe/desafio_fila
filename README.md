1) O arquivo .env foi retirado do .gitignore para facilitar o teste do app
2) Execute o comando 'docker-compose up' para rodar o rabbitMQ
3) Como ambiente virtual estou usando pipenv, então basta utilizar o comando -> pipenv shell
4) Para executar o programa basta usar o comando -> uvicorn main:app
5) Para acessar as rotas acesse no navegador -> localhost:8000/docs
6) Primeiro crie o banco de dados (fiz um rota para isso a fim de facilitar o uso)
**Pq SQLite
7) Crie e edite atendentes pelas rotas. Atenção aos modelos, principalmente referentes ao role (área de trabalho). Esses modelos estão no fim da página.
8) Crie novas solicitações
9) Escolha um atendente para buscar as solicitações
10) Finalize alguma solicitação