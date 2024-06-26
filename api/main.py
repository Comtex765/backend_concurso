from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud
from fastapi.middleware.cors import CORSMiddleware
from .database import get_db, test_db_connection
from typing import List

import requests

app = FastAPI(title="Comtex765", version="1.0.0")
test_db_connection()

# Permitir CORS para todos los dominios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto para permitir solo los dominios necesarios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    url = "https://api.countrystatecity.in/v1/countries/GB/states/EAY/cities"
    headers = {
        "X-CSCAPI-KEY": "QVZtQUl3aFQyejJwbW5qMFRPcVBiZGl6TDJjU2M2cmtTbHJoWFh3Tw=="
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto generará una excepción para códigos de error HTTP
        countries = response.json()  # Convertir la respuesta en JSON
        return countries  # Devolver los datos obtenidos
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching countries: {e}")
    # return {"Saludo": "Hola a todos ❤️"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, new_data: schemas.UserBase, db: Session = Depends(get_db)
):
    db_user = crud.update_user(db, user_id=user_id, new_data=new_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/countries", response_model=List[schemas.CountryBase])
def read_countries(db: Session = Depends(get_db)):
    countries = crud.get_countries(db)
    return countries


@app.get("/countries/{country_id}/states", response_model=schemas.CountryWithStates)
def read_states_by_country(country_id: int, db: Session = Depends(get_db)):
    country = crud.get_country(db, country_id=country_id)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    country.estados = crud.get_states_by_country(db, country_id=country_id)
    return country


@app.get("/states/{state_id}/cities", response_model=schemas.StateWithCities)
def read_cities_by_state(state_id: int, db: Session = Depends(get_db)):
    state = crud.get_state(db, state_id=state_id)
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")
    state.ciudades = crud.get_cities_by_state(db, state_id=state_id)
    return state
