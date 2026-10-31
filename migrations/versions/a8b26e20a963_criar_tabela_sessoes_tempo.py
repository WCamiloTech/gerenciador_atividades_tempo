
"""Criar tabela sessoes_tempo.

Revision ID: a8b26e20a963
Revises: 742c14add095
Create Date: 2026-10-31 12:55:23.237781
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.tipos import UTCDateTime


# Identificadores da migração.
revision: str = "a8b26e20a963"
down_revision: Union[str, Sequence[str], None] = "742c14add095"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Criar a tabela e seus índices."""

    op.create_table(
        "sessoes_tempo",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "atividade_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "inicio_em",
            UTCDateTime(),
            nullable=False,
        ),

        sa.Column(
            "fim_em",
            UTCDateTime(),
            nullable=True,
        ),

        sa.Column(
            "observacoes",
            sa.String(),
            nullable=True,
        ),

        sa.Column(
            "criada_em",
            UTCDateTime(),
            nullable=False,
        ),

        sa.Column(
            "atualizada_em",
            UTCDateTime(),
            nullable=False,
        ),

        sa.CheckConstraint(
            "fim_em IS NULL OR fim_em >= inicio_em",
            name="ck_sessoes_tempo_periodo_valido",
        ),

        sa.ForeignKeyConstraint(
            ["atividade_id"],
            ["atividades.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_sessoes_tempo_atividade_id",
        "sessoes_tempo",
        ["atividade_id"],
        unique=False,
    )

    op.create_index(
        "ix_sessoes_tempo_inicio_em",
        "sessoes_tempo",
        ["inicio_em"],
        unique=False,
    )

    op.create_index(
        "ux_sessoes_tempo_uma_aberta_por_atividade",
        "sessoes_tempo",
        ["atividade_id"],
        unique=True,
        sqlite_where=sa.text("fim_em IS NULL"),
    )


def downgrade() -> None:
    """Remover a tabela e seus índices."""

    op.drop_index(
        "ux_sessoes_tempo_uma_aberta_por_atividade",
        table_name="sessoes_tempo",
    )

    op.drop_index(
        "ix_sessoes_tempo_inicio_em",
        table_name="sessoes_tempo",
    )

    op.drop_index(
        "ix_sessoes_tempo_atividade_id",
        table_name="sessoes_tempo",
    )

    op.drop_table("sessoes_tempo")
