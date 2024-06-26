from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_atributes = True


class CityBase(BaseModel):
    id_ciudad: int
    nombre_ciudad: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    class Config:
        from_atributes = True


class StateBase(BaseModel):
    id_estado: int
    nombre_estado: str
    iso2: Optional[str] = None
    type_state: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    class Config:
        from_atributes = True


class CountryBase(BaseModel):
    id_pais: int
    nombre_pais: str
    iso2: Optional[str] = None
    iso3: Optional[str] = None
    phonecode: Optional[str] = None
    capital: Optional[str] = None
    currency: Optional[str] = None

    class Config:
        from_atributes = True


class CountryWithStates(CountryBase):
    estados: List[StateBase]


class StateWithCities(StateBase):
    ciudades: List[CityBase]
