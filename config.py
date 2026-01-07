import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://myuser:mypassword@db:3306/mydb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    API_KEY = "ecopackai-secret-key"
