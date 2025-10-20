from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import time

from app.config.settings import Settings
from app.database.models.user import table_registry

def _create_engine_with_retry(url: str, retries: int = 10, delay_seconds: int = 3):
    last_exc = None
    for _ in range(retries):
        try:
            return create_engine(url)
        except Exception as e:
            last_exc = e
            time.sleep(delay_seconds)
    raise last_exc

engine = _create_engine_with_retry(Settings().DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_session():
    with SessionLocal() as session:
        yield session


def create():
    """Criar todas as tabelas do banco de dados"""
    table_registry.metadata.create_all(bind=engine)


def init():
    """Iniciar o banco de dados"""
    create()
    print("Tabelas do banco de dados criadas com sucesso!")