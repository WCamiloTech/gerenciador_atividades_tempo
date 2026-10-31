
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.atividade import agora_utc
from app.tipos import UTCDateTime


class SessaoTempo(Base):
    __tablename__ = "sessoes_tempo"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    atividade_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("atividades.id"),
        nullable=False,
    )

    inicio_em: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        nullable=False,
        default=agora_utc,
    )

    fim_em: Mapped[datetime | None] = mapped_column(
        UTCDateTime(),
        nullable=True,
    )

    observacoes: Mapped[str | None] = mapped_column(
        String,
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

    __table_args__ = (
        CheckConstraint(
            "fim_em IS NULL OR fim_em >= inicio_em",
            name="ck_sessoes_tempo_periodo_valido",
        ),
        Index(
            "ix_sessoes_tempo_atividade_id",
            "atividade_id",
        ),
        Index(
            "ix_sessoes_tempo_inicio_em",
            "inicio_em",
        ),
        Index(
            "ux_sessoes_tempo_uma_aberta_por_atividade",
            "atividade_id",
            unique=True,
            sqlite_where=(fim_em.is_(None)),
        ),
    )
