import requests
import database as data


url = "https://api.countrystatecity.in/v1/countries"
headers = {"X-CSCAPI-KEY": "QVZtQUl3aFQyejJwbW5qMFRPcVBiZGl6TDJjU2M2cmtTbHJoWFh3Tw=="}


response = requests.get(url, headers=headers)
response.raise_for_status()  # Esto generará una excepción para códigos de error HTTP
countries = response.json()  # Convertir la respuesta en JSON


data.insert_countries_to_db(countries)
