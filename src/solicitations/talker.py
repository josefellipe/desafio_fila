from fastapi import HTTPException, status
from ..database.tables import Solicitation
from .models import SolicitationModel, SolicitationCreateUpdateModel, SolicitationPatchModel
from ..database.connection import DatabaseManager

from typing import List

class Solicitations:
    def __init__(self) -> None:
        self.db = DatabaseManager()
        self.session = self.db.open_session()

        
    def create_solicitation(self, solicitation: SolicitationCreateUpdateModel) -> SolicitationModel:
        solicitation = Solicitation(**solicitation.__dict__)
        self.session.add(solicitation)
        self.session.commit()
        self.session.refresh(solicitation)
        self.db.close_session()
        return SolicitationModel(**solicitation.__dict__)


    def read_solicitations(self, skip: int = 0, limit: int = 5) -> List[SolicitationModel]:
        solicitations = self.session.query(Solicitation).offset(skip).limit(limit).all()
        self.db.close_session()
        return [SolicitationModel(**solicitation.__dict__) for solicitation in solicitations]


    def read_solicitation(self, solicitation_id: int) -> SolicitationModel:
        solicitation = self.session.get(Solicitation, solicitation_id)
        if solicitation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitation not found")
        
        return SolicitationModel(**solicitation.__dict__)


    def update_solicitation(self, solicitation_id: int, solicitation_patch: SolicitationPatchModel) -> SolicitationModel:
        count = 0
        for field, value in solicitation_patch.__dict__.items():
            if value:
                count += 1
        if count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field is required")
        
        solicitation = self.session.get(Solicitation, solicitation_id)
        if solicitation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitation not found")


        for field, value in solicitation_patch.__dict__.items():
            if value is not None:
                setattr(solicitation, field, value)

        self.session.commit()
        self.session.refresh(solicitation)
        self.db.close_session()
        return SolicitationModel(**solicitation.__dict__)


    def delete_solicitation(self, solicitation_id: int) -> SolicitationModel:
        solicitation = self.session.get(Solicitation, solicitation_id)
        if solicitation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitation not found")
        
        self.session.delete(solicitation)
        self.session.commit()
        return "Solicitation deleted successfully"