import uuid

from sqlalchemy import Boolean, String, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cor: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    __table_args__ = (
        Index(
            "ix_categorias_nome_unico",
            func.lower(nome),
            unique=True,
        ),
    )