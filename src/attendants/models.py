from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union
from enum import Enum

class AttendantRoleEnum(str, Enum):
    cartoes = "Cartões"
    emprestimos = "Empréstimos"
    outros = "Outros Assuntos"

class AttendantCreateUpdateModel(BaseModel):
    name: Optional[str] = None
    cpf: str
    role: Union[AttendantRoleEnum, str]

    is_active: bool = True

class AttendantModel(AttendantCreateUpdateModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AttendantPatchModel(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    role: Optional[Union[AttendantRoleEnum, str]] = None

    is_active: Optional[bool] = None
