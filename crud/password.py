from core import config
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import password as models
from core.security import get_password_hash, verify_password


# ---------------- READ PASSWORDS -------------------------- #

def get_password_by_user(db: Session, user_uuid: str):
    passwords = db.query(models.Password).filter(
        models.Password.user_uuid == user_uuid).order_by(
        models.Password.created_date.desc()).all()
    return passwords


# ---------------- CREATE PASSWORD -------------------------- #

def create_user_password(db: Session, password: str, user_uuid: str):
    hashed_password = get_password_hash(password)
    db_password = models.Password(
        user_uuid=str(user_uuid),
        password=hashed_password,
    )
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


# ---------------- UPDATE PASSWORD -------------------------- #

def update_password(db: Session, password: str, user_uuid: str):
    data = get_password_by_user(db, user_uuid)
    limit = int(config.PASSWORD_LIMIT)
    for r in data:
        if verify_password(password, r.password):
            raise HTTPException(
                status_code=400,
                detail=f"Password should not match with previous {limit} passwords used")
    if len(data) >= limit:
        passwords = db.query(models.Password.id).filter(
            models.Password.user_uuid == user_uuid).order_by(
            models.Password.created_date.desc()).offset(limit-1).subquery()
        db.query(models.Password).filter(
            models.Password.id.in_(passwords)).delete(synchronize_session=False)
        db.commit()
    create_user_password(db, password, user_uuid)
    return "deleted old password"


# ---------------- DELETE PASSWORD -------------------------- #

def delete_password(db: Session, user_uuid: str):
    db.query(models.Password).filter(
        models.Password.user_uuid == user_uuid).delete(synchronize_session=False)
    db.commit()
    return "delete all passwords for the user"
