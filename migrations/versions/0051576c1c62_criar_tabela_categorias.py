"""Criar tabela categorias.

Revision ID: 0051576c1c62
Revises:
Create Date: 2026-10-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificadores da migração
revision: str = "0051576c1c62"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Criar a tabela categorias e seu índice único."""

    op.create_table(
        "categorias",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("cor", sa.String(length=20), nullable=True),
        sa.Column("ativa", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Impede nomes duplicados ignorando maiúsculas/minúsculas.
    op.create_index(
        "ix_categorias_nome_unico",
        "categorias",
        [sa.text("lower(nome)")],
        unique=True,
    )


def downgrade() -> None:
    """Desfazer a criação da tabela categorias."""

    op.drop_index(
        "ix_categorias_nome_unico",
        table_name="categorias",
    )

    op.drop_table("categorias")