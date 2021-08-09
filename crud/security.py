from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import security as models
from schemas import security as schemas


def get_logins(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.SecurityOut]:
    login = db.query(models.Security).offset(skip).limit(limit).all()
    if not login:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Login not found")
    return login


def get_login(db: Session, email: int, skip: int = 0, limit: int = 100) -> List[schemas.SecurityOut]:
    login = db.query(models.Security).filter(
        models.Security.email == email).order_by(models.Security.time.desc()).offset(skip).limit(limit).all()
    if not login:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Login not found")
    return login


def create_login(db: Session, login: schemas.SecurityCreate):
    db_login = models.Security(
        email=login.email,
        device=login.device,
        os=login.os,
        ip=login.ip,
        city=login.city,
        region=login.region,
        country_name=login.country_name,
        postal=login.postal,
        latitude=login.latitude,
        longitude=login.longitude,
        org=login.org,
    )
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login
