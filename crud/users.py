from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from models import users as models
from schemas import users as schemas
from core.security import get_password_hash
from core import jsonencoder as encoder
from core import config

root_user = config.ROOT_USER
root_user_password = config.ROOT_USER_PASSWORD


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.UserOut]:
    users = db.query(models.User).offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="No records found")
    return users


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    check = db.query(models.User).filter(
        models.User.email == user.email).first()
    if check:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_rootuser(db: Session):
    hashed_password = get_password_hash(root_user_password)
    check = db.query(models.User).filter(
        models.User.email == root_user).first()
    if check:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = models.User(
        first_name='Root',
        last_name='Admin',
        email=root_user,
        is_active=True,
        is_superuser=True,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    usercheck = json.dumps(user, cls=encoder.AlchemyEncoder)
    usercheck = json.loads(usercheck)
    if usercheck['email'] == root_user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Root User can't be deleted")
    db.delete(user)
    db.commit()
    return user


def edit_user(db: Session, user_id: int, user: schemas.UserEdit) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    usercheck = json.dumps(db_user, cls=encoder.AlchemyEncoder)
    usercheck = json.loads(usercheck)
    if usercheck['email'] == root_user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Root User can't be edited")

    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
