from pydantic import root_validator, BaseSettings
import sys, os
from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv
load_dotenv()



class Settings(BaseSettings):

    DB_HOST=os.getenv('DB_HOST')
    DB_PORT=os.getenv('DB_PORT') #5432
    DB_USER=os.getenv('DB_USER')
    DB_PASS=os.getenv('DB_PASS')
    DB_NAME=os.getenv('DB_NAME') #default_db

    KAFKA_HOST:str=os.getenv('KAFKA_HOST')
    KAFKA_PORT:int=os.getenv('KAFKA_PORT')

    FILE_SERVER_HOST:str = os.getenv('FILE_SERVER_HOST')


    FCM_REGISTRATION_API:str = os.getenv('FCM_REGISTRATION_API')
    HCM_APP_ID:str = os.getenv('HCM_APP_ID')
    HCM_APP_SECRET:str = os.getenv('HCM_APP_SECRET')

    jwt_secret: str = os.getenv('JWT_SECRET')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM')
    jwt_expires_s: int = os.getenv('JWT_EXPIRES_S')


 

    
    @root_validator
    def get_database_url(cls,v):
        v["DATABASE_URL"]= f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v

    class Config:
        env_file = '.env'

settings = Settings()

