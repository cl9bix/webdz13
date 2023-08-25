from pydantic import BaseSettings


class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
    DB_URL = 'postgresql+asyncpg://user:5671234@localhost:5432/todo_db'

    


config = Config


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379


settings = Settings()


