import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://ecopack:ecopack123@ecopack-db:5432/ecopack_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_KEY = os.getenv("ECOPACK_API_KEY", "ecopack-secret-key")
