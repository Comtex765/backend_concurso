from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base
import bcrypt


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    def verify_password(self, password: str):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    @staticmethod
    def generate_hashed_password(password: str):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


class Country(Base):
    __tablename__ = "pais"

    id_pais = Column(Integer, primary_key=True, index=True)
    nombre_pais = Column(String)
    iso2 = Column(String)
    iso3 = Column(String)
    phonecode = Column(String)
    capital = Column(String)
    currency = Column(String)

    # Relationship to states, useful for ORM querying
    estados = relationship("State", back_populates="pais")


class State(Base):
    __tablename__ = "estado"

    id_estado = Column(Integer, primary_key=True, index=True)
    nombre_estado = Column(String)
    id_pais = Column(Integer, ForeignKey("pais.id_pais"))
    cod_pais = Column(String(2))
    iso2 = Column(String(2))
    type_state = Column(String(50), nullable=True)
    latitude = Column(String(50))
    longitude = Column(String(50))

    # Relationship to country, useful for ORM querying
    pais = relationship("Country", back_populates="estados")
    ciudades = relationship("City", back_populates="estado")


class City(Base):
    __tablename__ = "ciudad"

    id_ciudad = Column(Integer, primary_key=True, index=True)
    nombre_ciudad = Column(String(50))
    id_estado = Column(Integer, ForeignKey("estado.id_estado"))
    latitude = Column(String(50))
    longitude = Column(String(50))

    estado = relationship("State", back_populates="ciudades")
