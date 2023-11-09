from fastapi import APIRouter, HTTPException, Depends, Response, status
from ..solicitations.models import SolicitationModel, SolicitationCreateUpdateModel, SolicitationPatchModel
from ..util.autorizations import verify_key_and_user

import json

from ..util.queue import Queue


from typing import List

solicitations_route = APIRouter()


@solicitations_route.post("/solicitation/")
def create_new_solicitation(solicitation: SolicitationCreateUpdateModel, key: tuple = Depends(verify_key_and_user)):
    queue = Queue()
    queue.send_to_queue(message=json.dumps(solicitation.__dict__, ensure_ascii=False).encode('utf-8'), queue_name=solicitation.solicitation_type)
    queue_size = queue.get_queue_size(queue_name=solicitation.solicitation_type)
    print(queue_size)
    queue.connection.close()
    return Response(content=f"The solicitation has send to queue", status_code=status.HTTP_200_OK)



#    queue = Queue()
#    print(queue.consume_next_message(queue_name=solicitation.solicitation_type))