from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    # Configuração base do banco
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "senha123"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "websocket_fibonacci"

    @property
    def DATABASE_URL(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASSWORD)
        host = self.DB_HOST
        port = self.DB_PORT
        db = self.DB_NAME
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    HOST: str = "0.0.0.0"
    PORT: int = 8000