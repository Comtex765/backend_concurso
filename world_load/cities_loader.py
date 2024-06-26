import requests
import database as data
import time

MAX_RETRIES = 3


def load_ciudades_from_api_with_retries(country_code: str, state_code: str):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}/cities"
    headers = {
        "X-CSCAPI-KEY": "QVZtQUl3aFQyejJwbW5qMFRPcVBiZgl6TDJjU2M2cmtTbHJoWFh3Tw=="
    }

    print(f"GET:    {url}")

    for retry in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Manejar errores HTTP

            ciudades = response.json()  # Convertir la respuesta en JSON
            return ciudades

        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP en el intento {retry + 1}: {http_err}")
            if retry < MAX_RETRIES - 1:
                print("Reintentando...")
                time.sleep(5)  # Esperar 5 segundos antes de reintentar
                continue
            else:
                return None

        except requests.exceptions.RequestException as req_err:
            print(f"Error de solicitud en el intento {retry + 1}: {req_err}")
            if retry < MAX_RETRIES - 1:
                print("Reintentando...")
                time.sleep(5)  # Esperar 5 segundos antes de reintentar
                continue
            else:
                return None

    return None  # Si todos los intentos fallan


def main():
    db = data.SessionLocal()

    try:
        countries = data.get_all_countries(db)

        for country in countries:
            states = data.get_states_by_country(db, country.id_pais)

            for state in states:
                if not data.ciudades_ya_cargadas(db, country.id_pais, state.id_estado):
                    ciudades = load_ciudades_from_api_with_retries(
                        country.iso2, state.iso2
                    )

                    # Agrega una barra de progreso para el bucle de ciudades
                    for ciudad in ciudades:
                        # Agregar el ID del país y estado a los datos de la ciudad
                        ciudad["country_id"] = country.id_pais
                        ciudad["state_id"] = state.id_estado

                    data.insert_ciudades_to_db(db, ciudades)
                else:
                    pass

    except Exception as e:
        print(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
