from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from app.config import settings


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    metadata = MetaData(
        naming_convention=settings.database.naming_convention,
    )
