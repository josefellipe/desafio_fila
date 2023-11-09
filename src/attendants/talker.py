from fastapi import APIRouter, HTTPException, Depends
from ..database.tables import Attendant, Solicitation
from .models import AttendantModel, AttendantCreateUpdateModel, AttendantPatchModel
from ..solicitations.models import SolicitationModel, SolicitationCreateUpdateModel, SolicitationPatchModel
from ..database.connection import DatabaseManager
from ..util.autorizations import verify_key_and_user

from typing import List

attendant_route = APIRouter()


@attendant_route.post("/attendants/", response_model=AttendantModel)
def create_attendant(attendant: AttendantCreateUpdateModel, key: tuple = Depends(verify_key_and_user)):
    db = DatabaseManager()
    session = db.open_session()
    attendant = Attendant(**attendant.__dict__)
    session.add(attendant)
    session.commit()
    session.refresh(attendant)
    db.close_session()
    return AttendantModel(**attendant.__dict__)

@attendant_route.get("/attendants/", response_model=List[AttendantModel])
def read_attendants(skip: int = 0, limit: int = 5, key: str = Depends(verify_key_and_user)):
    db = DatabaseManager()
    session = db.open_session()
    attendants = session.query(Attendant).offset(skip).limit(limit).all()
    db.close_session()
    return [AttendantModel(**attendant.__dict__) for attendant in attendants]

@attendant_route.get("/attendants/{attendant_id}", response_model=AttendantModel)
def read_attendant(attendant_id: int, key: str = Depends(verify_key_and_user)):
    db = DatabaseManager()
    session = db.open_session()
    attendant = session.get(Attendant, attendant_id)
    if attendant is None:
        raise HTTPException(status_code=404, detail="Attendant not found")
    
    return AttendantModel(**attendant.__dict__)

@attendant_route.patch("/attendants/{attendant_id}", response_model=AttendantModel)
def update_attendant(attendant_id: int, attendant_patch: AttendantPatchModel, key: str = Depends(verify_key_and_user)):
    count = 0
    for field, value in attendant_patch.__dict__.items():
        if value:
            count =+ 1
    if count == 0:
        raise HTTPException(status_code=400, detail="Necessário ao menos um campo para alterar")
    
    db = DatabaseManager()
    session = db.open_session()
    attendant = session.get(Attendant, attendant_id)
    if attendant is None:
        raise HTTPException(status_code=404, detail="Attendant not found")


    for field, value in attendant_patch.__dict__.items():
        if value is not None:
            setattr(attendant, field, value)

    session.commit()
    session.refresh(attendant)
    db.close_session()
    return AttendantModel(**attendant.__dict__)

@attendant_route.delete("/attendants/{attendant_id}", response_model=AttendantModel)
def delete_attendant(attendant_id: int, key: str = Depends(verify_key_and_user)):
    db = DatabaseManager()
    session = db.open_session()
    attendant = session.get(Attendant, attendant_id)
    if attendant is None:
        raise HTTPException(status_code=404, detail="Attendant not found")
    
    session.delete(attendant)
    session.commit()
    return AttendantModel(**attendant.__dict__)