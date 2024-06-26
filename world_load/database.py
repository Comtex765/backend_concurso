from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from colorama import Fore, Style
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from models import Country, State, City
from sqlalchemy.orm import Session


import os
import psycopg2.errors

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_DIALECT = os.getenv("DB_DIALECT")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
SQLALCHEMY_DATABASE_URL = "{}://{}:{}@[{}]/{}".format(
    DB_DIALECT, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
)

print(
    f"\n{Fore.CYAN}INFO:{Style.RESET_ALL}     ❤️  DataBase URL connection ==> {SQLALCHEMY_DATABASE_URL} ❤️",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_countries_to_db(countries: list):
    db = SessionLocal()  # Obtener una nueva sesión de la fábrica

    try:
        for country_data in countries:
            country = Country(
                id_pais=country_data["id"],
                nombre_pais=country_data["name"],
                iso2=country_data["iso2"],
                iso3=country_data["iso3"],
                phonecode=country_data["phonecode"],
                capital=country_data["capital"],
                currency=country_data["currency"],
            )
            db.add(country)

        db.commit()  # Confirmar los cambios en la base de datos

    except Exception as e:
        db.rollback()  # Revertir cambios en caso de error
        raise e

    finally:
        db.close()  # Cerrar la sesión de manera segura al finalizar


def insert_estados_to_db(db: Session, estados: list):
    try:
        for estado_data in estados:
            estado = State(
                id_estado=estado_data["id"],
                nombre_estado=estado_data["name"],
                id_pais=estado_data["country_id"],
                cod_pais=estado_data["country_code"],
                iso2=estado_data["iso2"],
                type_state=estado_data["type"],
                latitude=estado_data["latitude"],
                longitude=estado_data["longitude"],
            )
            db.add(estado)

        db.commit()  # Confirmar los cambios en la base de datos

    except Exception as e:
        db.rollback()  # Revertir cambios en caso de error
        raise e

    finally:
        db.close()  # Cerrar la sesión de manera segura al finalizar


def get_all_countries(db: Session):
    return db.query(Country).all()


def get_states_by_country(db: Session, country_id: int):
    return db.query(State).filter(State.id_pais == country_id).all()


def ciudades_ya_cargadas(db: Session, country_id: int, state_id: int) -> bool:
    return (
        db.query(City)
        .filter(City.id_pais == country_id, City.id_estado == state_id)
        .count()
        > 0
    )


def insert_ciudades_to_db(db: Session, ciudades: list):
    try:
        for ciudad_data in ciudades:
            try:
                ciudad = City(
                    id_ciudad=ciudad_data["id"],
                    nombre_ciudad=ciudad_data["name"],
                    id_pais=ciudad_data["country_id"],
                    id_estado=ciudad_data["state_id"],
                    latitude=ciudad_data["latitude"],
                    longitude=ciudad_data["longitude"],
                )
                db.add(ciudad)
                db.commit()  # Confirmar los cambios para cada ciudad
            except IntegrityError as e:
                db.rollback()  # Revertir cambios si ocurre un error
                if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                    pass
                else:
                    raise e
                return False
    finally:
        db.close()  # Cerrar la sesión de manera segura al finalizar
    return True
