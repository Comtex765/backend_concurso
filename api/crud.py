from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    encripatada = models.User.generate_hashed_password(user.password)
    db_user = models.User(username=user.username, password=encripatada)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, new_data: schemas.UserBase):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = new_data.username
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Country operations
def get_country(db: Session, country_id: int):
    return db.query(models.Country).filter(models.Country.id_pais == country_id).first()


def get_countries(db: Session):
    return db.query(models.Country).all()


# State operations
def get_state(db: Session, state_id: int):
    return db.query(models.State).filter(models.State.id_estado == state_id).first()


def get_states_by_country(db: Session, country_id: int):
    return db.query(models.State).filter(models.State.id_pais == country_id).all()


# City operations
def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id_ciudad == city_id).first()


def get_cities_by_state(db: Session, state_id: int):
    return db.query(models.City).filter(models.City.id_estado == state_id).all()
