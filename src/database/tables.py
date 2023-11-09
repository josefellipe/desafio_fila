from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Attendant(Base):
    __tablename__ = 'attendant'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100), nullable=False)
    cpf         = Column(String(20), nullable=False, unique=True)
    role        = Column(String(20), nullable=False)

    is_active   = Column(Boolean, default=True)

    created_at  = Column(DateTime, default=datetime.now)
    updated_at  = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Solicitation(Base):
    __tablename__ = 'solicitation'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    solicitation_type   = Column(String(20), nullable=False)
    description         = Column(String(400), nullable=False)

    is_to_do            = Column(Boolean, default=True)
    is_doing            = Column(Boolean, default=False)
    is_done             = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    attendant_id = Column(Integer, ForeignKey('attendant.id'))

