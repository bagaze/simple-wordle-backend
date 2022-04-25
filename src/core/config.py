from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = '/api'
    PROJECT_NAME: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
