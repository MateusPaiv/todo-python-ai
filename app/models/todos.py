import enum
import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.session import Base
from .user import UserRead


class TodoStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), primary_key=True,
                server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TodoStatus), nullable=False,
                    default=TodoStatus.pending)
    due_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="todos")


class TodoCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    user_id: str


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
    due_date: datetime | None = None


class TodoResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: TodoStatus
    due_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoDelete(BaseModel):
    message: str


class TodoRead(BaseModel):
    title: str
    description: str
    status: TodoStatus
    due_date: datetime
    created_at: datetime
    updated_at: datetime
    user: UserRead

    class Config:
        from_attributes = True
        from_attributes = True
