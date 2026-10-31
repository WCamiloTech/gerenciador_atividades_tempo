import uuid

from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.tipos import UTCDateTime


def agora_utc():
    """Retorna a data e hora atual em UTC."""
    return datetime.now(timezone.utc)


class Atividade(Base):
    __tablename__ = "atividades"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    titulo: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sobre: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    categoria_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("categorias.id"),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="em_andamento",
    )

    origem: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="espontanea",
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    link: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    criada_em: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
        default=agora_utc,
    )

    atualizada_em: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
        default=agora_utc,
        onupdate=agora_utc,
    )

    excluida_em: Mapped[datetime | None] = mapped_column(
        UTCDateTime(),
        nullable=True,
    )