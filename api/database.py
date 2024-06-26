from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from colorama import Fore, Style

import webbrowser
import os

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


def test_db_connection():
    try:
        # Intenta crear una sesión
        db = SessionLocal()
        # Ejecuta una consulta simple para probar la conexión
        db.execute(text("SELECT 1"))
        db.close()

        print(
            f"{Fore.CYAN}INFO:{Style.RESET_ALL}     ❤️  Test connection successfully ❤️\n"
        )

        url = "http:127.0.0.1:8000/docs"
        # webbrowser.open(url)

    except Exception as e:
        print(
            f"{Fore.RED}ERROR:{Style.RESET_ALL}     ❤️  Test connection failed: {e} ❤️\n"
        )
