from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str = "postgresql://postgres:senha123@localhost:5432/websocket_fibonacci"
    HOST: str = "0.0.0.0"
    PORT: int = 8000