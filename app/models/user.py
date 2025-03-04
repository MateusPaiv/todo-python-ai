import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    phone = Column(String(15), nullable=True)

    todos = relationship("Todo", back_populates="user")


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserDelete(BaseModel):
    message: str


class UserRead(BaseModel):
    name: str
    email: str
    phone: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
