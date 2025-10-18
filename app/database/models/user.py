from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, mapped_as_dataclass, registry
from sqlalchemy import func, String
from datetime import datetime

table_registry = registry()

@mapped_as_dataclass(table_registry)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))
    connected: Mapped[bool]
    connected_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    disconnected_at: Mapped[datetime]