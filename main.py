from fastapi import FastAPI
from src.attendants.talker import attendant_route
from src.mappers.new_solicitation import solicitations_route
from src.mappers.solicitation_resoluction import resoluction_route
from src.util.create_db import create_db_route

import uvicorn

from decouple import config

app = FastAPI()

app.include_router(solicitations_route)
app.include_router(resoluction_route)
app.include_router(attendant_route)
app.include_router(create_db_route)

if __name__ == "__main__":
    uvicorn.run(
        app     = app, 
        host    = config('HOST'), 
        port    = config('PORT')
    )