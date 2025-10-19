from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import Settings
from app.database.models.user import table_registry

engine = create_engine(Settings().DATABASE_URL)

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