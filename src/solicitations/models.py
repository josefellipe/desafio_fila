from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class SolicitationTypeEnum(Enum):
    cartoes = "Problemas com cartão"
    emprestimos = "Contratação de empréstimo"
    outros = "Outros Assuntos"

class SolicitationQueueModel(BaseModel):
    solicitation_type: Optional[str] = None
    description: str

class SolicitationCreateUpdateModel(BaseModel):
    solicitation_type: Optional[str] = None
    description: str

    is_to_do: bool = False
    is_doing: bool = True
    is_done: bool = False

    attendant_id: Optional[int] = None


class SolicitationModel(SolicitationCreateUpdateModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SolicitationPatchModel(BaseModel):
    solicitation_type: Optional[str] = None
    description: Optional[str] = None

    is_to_do: Optional[bool] = None
    is_doing: Optional[bool] = None
    is_done: Optional[bool] = None

    attendant_id: Optional[int] = None
