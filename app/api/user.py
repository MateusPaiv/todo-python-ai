from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models.user import UserCreate, UserRead, User, UserUpdate
from ..core.secutiry import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> UserRead:
    if_existis = db.query(User).filter(User.email == user.email).first()

    if if_existis:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str, user: UserUpdate, db: Annotated[Session, Depends(get_db)]
) -> UserRead:
    user_to_update = db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(user_to_update, field, value)

    db.commit()
    db.refresh(user_to_update)

    return user_to_update


@router.get("/", response_model=list[UserRead])
def get_users(db: Annotated[Session, Depends(get_db)]) -> list[UserRead]:
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Annotated[Session, Depends(get_db)]) -> UserRead:
    user = db.query(User).filter(User.id == user_id).first()
    return user
