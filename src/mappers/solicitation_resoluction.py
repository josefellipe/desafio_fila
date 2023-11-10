from fastapi import APIRouter, Depends, Response, status
from ..solicitations.models import SolicitationModel, SolicitationCreateUpdateModel, SolicitationPatchModel
from ..util.autorizations import verify_key_and_user
from ..attendants.models import AttendantRoleEnum

from ..attendants.talker import read_attendant
from ..solicitations.talker import Solicitations

import json
from typing import List
from decouple import config

from ..util.queue import Queue

resoluction_route = APIRouter()


@resoluction_route.post("/resoluction/")
def attendante_get_solicitation(attendant_id: int, key: tuple = Depends(verify_key_and_user)):
    key = {'API_USER':config('API_USER'), 'API_PASSWORD': config('API_PASSWORD')}
    attendant = read_attendant(attendant_id=attendant_id, key=key)
    solicitations_db = Solicitations()
    solicitations_attendant = len(solicitations_db.read_solicitations_by_attendant_doing(attendant_id=attendant.id))
    queue = Queue()
    new_solicitation = None
    while solicitations_attendant < 3:
        queue_size = queue.get_queue_size(queue_name=f'{attendant.role}')
        print(queue_size)
        if int(queue_size) == 0:
            break
        
        solicitation = queue.consume_next_message(queue_name=attendant.role)
        new_solicitation = SolicitationCreateUpdateModel(**json.loads(solicitation['message']), attendant_id=attendant_id)
        if new_solicitation.solicitation_type == 'Problemas com cartão':
            new_solicitation.solicitation_type = AttendantRoleEnum.cartoes.value
        elif new_solicitation.solicitation_type == 'Contratação de empréstimo':
            new_solicitation.solicitation_type = AttendantRoleEnum.emprestimos.value
        else:
            new_solicitation.solicitation_type = AttendantRoleEnum.outros.value

        solicitations_db.create_solicitation(new_solicitation)
        solicitations_attendant += 1

    if new_solicitation:
        solicitations_db.close_session()
    
    return Response(content=f"Attendant is full", status_code=status.HTTP_200_OK)


@resoluction_route.get("/resoluction/attendant_doing/{attendant_id}")
def get_solicitations_doing_by_attendante(attendant_id: str, key: tuple = Depends(verify_key_and_user)) -> List[SolicitationModel]:
    key = {'API_USER':config('API_USER'), 'API_PASSWORD': config('API_PASSWORD')}
    attendant = read_attendant(attendant_id=int(attendant_id), key=key)
    solicitations_db = Solicitations()
    solicitations_attendant = solicitations_db.read_solicitations_by_attendant_doing(attendant_id=attendant.id)

    solicitations_db.close_session()
    return [SolicitationModel(**solicitation.__dict__) for solicitation in solicitations_attendant]


@resoluction_route.get("/resoluction/change_solicitation_done/{solicitation_id}")
def change_solicitation_to_done(solicitation_id: str, key: tuple = Depends(verify_key_and_user)) -> List[SolicitationModel]:
    key = {'API_USER':config('API_USER'), 'API_PASSWORD': config('API_PASSWORD')}
    solicitations_db = Solicitations()
    solicitation_updated = SolicitationPatchModel(
        is_to_do = False,
        is_doing = False,
        is_done = True
        )
    solicitations_db.update_solicitation(solicitation_id, solicitation_updated)

    attendante_id = solicitations_db.read_solicitation(solicitation_id).attendant_id
    attendante_get_solicitation(attendant_id=attendante_id, key=key)

    solicitations_db.close_session()
    return Response(content=f"Solicitation is complete", status_code=status.HTTP_200_OK)

