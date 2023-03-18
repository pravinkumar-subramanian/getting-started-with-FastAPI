from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
import json
import uuid

from models import users as models
from schemas import users as schemas
from crud.password import create_user_password, update_password, delete_password
from core.security import get_password_hash
from core import jsonencoder as encoder
from core import config

root_user = config.ROOT_USER
root_user_password = config.ROOT_USER_PASSWORD
root_password_expiry = 365
password_expiry = int(config.PASSWORD_EXPIRY)

# ---------------- READ USERS -------------------------- #


def get_user(db: Session, user_id: str):
    user = db.query(models.User).filter(
        models.User.user_uuid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    user = db.query(models.User).filter(
        func.lower(models.User.email) == email.lower()).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username / email")
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.User]:
    users = db.query(models.User).offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="No records found")
    return users


# ---------------- CREATE USERS -------------------------- #

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    check = db.query(models.User).filter(
        func.lower(models.User.email) == user.email.lower()).first()
    if check:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = models.User(
        user_uuid=str(uuid.uuid4()),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email.lower(),
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
        expires_on=datetime.utcnow() + timedelta(days=password_expiry)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_user_password(db, user.password, db_user.user_uuid)
    return db_user


def create_rootuser(db: Session):
    hashed_password = get_password_hash(root_user_password)
    check = db.query(models.User).filter(
        func.lower(models.User.email) == root_user.lower()).first()
    if check:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = models.User(
        user_uuid=str(uuid.uuid4()),
        first_name='Root',
        last_name='Admin',
        email=root_user.lower(),
        is_active=True,
        is_superuser=True,
        hashed_password=hashed_password,
        expires_on=datetime.utcnow() + timedelta(days=root_password_expiry)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    create_user_password(db, root_user_password, db_user.user_uuid)
    return db_user


# ---------------- DELETE USERS -------------------------- #

def delete_user(db: Session, user_uuid: str):
    user = get_user(db, user_uuid)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Can't delete: User not found")
    usercheck = json.dumps(user, cls=encoder.AlchemyEncoder)
    usercheck = json.loads(usercheck)
    if usercheck['email'] == root_user.lower():
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Root User can't be deleted")
    db.delete(user)
    db.commit()
    delete_password(db, user_uuid)
    return user


# ---------------- EDIT USERS -------------------------- #

def edit_user(db: Session, user_uuid: str, user: schemas.UserEdit) -> schemas.User:
    db_user = get_user(db, user_uuid)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Can't edit: User not found")
    # check for rootuser
    usercheck = json.dumps(db_user, cls=encoder.AlchemyEncoder)
    usercheck = json.loads(usercheck)
    if usercheck['email'] == root_user.lower():
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Root User can't be edited")
    # check for edit paramters
    update_data = user.dict(exclude_unset=True)
    if update_data:
        update_data['last_modified'] = datetime.utcnow()
    else:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Provide proper parameters to edit")
    # add paramters
    if 'is_active' in update_data:
        update_data['login_attempt'] = 0 if update_data['is_active'] != usercheck['is_active'] else usercheck['login_attempt']
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        update_data["expires_on"] = datetime.utcnow() + \
            timedelta(days=password_expiry)
        del update_data["password"]
        update_password(db, user.password, user_uuid)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
