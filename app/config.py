""" Loading and validation of all environment variables and secrets """

# Imports
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

# Loading .env file
load_dotenv('local.env')


class AppSettings(BaseSettings):
    """ App Settings schema """
    title: str = "Chitros"
    description: str = "Social media backend API made using FastAPI"
    version: str = "0.0.1"


class Settings(BaseSettings):
    """ Settings schema """
    database_username: str
    database_server: str
    database_password: str
    database_hostname: str
    database_name: str
    database_port: int
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cors_origin_whitelist: str

    @validator('cors_origin_whitelist')
    def split_cors_origin_string(cls, cors_origin_whitelist):
        """ Convert cors_origin_whitelist string to list """

        return cors_origin_whitelist.split(',')

    class Config:
        """ Link env file name """
        env_file = ".\local.env"


app_settings = AppSettings()
settings = Settings()
