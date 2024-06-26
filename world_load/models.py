from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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
    ciudades = relationship("City", back_populates="pais")


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
    id_pais = Column(Integer, ForeignKey("pais.id_pais"))
    id_estado = Column(Integer, ForeignKey("estado.id_estado"))
    latitude = Column(String(50))
    longitude = Column(String(50))

    pais = relationship("Country", back_populates="ciudades")
    estado = relationship("State", back_populates="ciudades")
