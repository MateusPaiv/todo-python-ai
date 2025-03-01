from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..db.session import get_db
from ..models.todos import Todo, TodoCreate, TodoRead, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo: TodoCreate, db: Annotated[Session, Depends(get_db)]
) -> TodoResponse:

    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        user_id=todo.user_id,
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/", response_model=list[TodoRead])
def get_todos(db: Annotated[Session, Depends(get_db)]) -> list[TodoRead]:
    todos = db.query(Todo).options(joinedload(Todo.user)).all()
    return todos


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: str, db: Annotated[Session, Depends(get_db)]) -> TodoRead:
    todo = db.query(Todo).options(joinedload(Todo.user)
                                  ).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: str, todo: TodoUpdate, db: Annotated[Session, Depends(get_db)]
) -> TodoResponse:
    todo_to_update = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_to_update:
        raise HTTPException(status_code=404, detail="Todo not found")

    for field, value in todo.model_dump(exclude_unset=True).items():
        setattr(todo_to_update, field, value)

    db.commit()
    db.refresh(todo_to_update)

    return todo_to_update
