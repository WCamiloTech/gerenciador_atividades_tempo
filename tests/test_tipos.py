from datetime import datetime, timedelta, timezone

import pytest

from sqlalchemy import create_engine
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Atividade


@pytest.fixture
def banco_teste(tmp_path):
    """Cria um banco SQLite temporário para testar datas."""

    caminho = tmp_path / "teste_utc.db"

    engine = create_engine(
        f"sqlite:///{caminho.as_posix()}"
    )

    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()


def test_armazenar_data_utc(banco_teste):
    """Verifica se uma data UTC é recuperada corretamente."""

    data_original = datetime(
        2026, 10, 30, 18, 0,
        tzinfo=timezone.utc,
    )

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Teste UTC",
            criada_em=data_original,
        )

        sessao.add(atividade)
        sessao.commit()

        atividade_id = atividade.id

    with Session(banco_teste) as sessao:
        recuperada = sessao.get(
            Atividade,
            atividade_id,
        )

        assert recuperada is not None
        assert recuperada.criada_em == data_original
        assert recuperada.criada_em.tzinfo == timezone.utc


def test_converter_utc_menos_tres(banco_teste):
    """Converte um horário UTC-3 para UTC."""

    fuso_brasilia = timezone(timedelta(hours=-3))

    data_local = datetime(
        2026, 10, 30, 15, 0,
        tzinfo=fuso_brasilia,
    )

    data_esperada = datetime(
        2026, 10, 30, 18, 0,
        tzinfo=timezone.utc,
    )

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Teste de conversão",
            criada_em=data_local,
        )

        sessao.add(atividade)
        sessao.commit()

        atividade_id = atividade.id

    with Session(banco_teste) as sessao:
        recuperada = sessao.get(
            Atividade,
            atividade_id,
        )

        assert recuperada is not None
        assert recuperada.criada_em == data_esperada
        assert recuperada.criada_em.tzinfo == timezone.utc


def test_rejeitar_data_sem_fuso(banco_teste):
    """Impede o armazenamento de datas sem fuso horário."""

    data_sem_fuso = datetime(
        2026, 10, 30, 15, 0
    )

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Data inválida",
            criada_em=data_sem_fuso,
        )

        sessao.add(atividade)

        with pytest.raises(StatementError) as erro:
            sessao.commit()

        # Confirma que o erro original foi um ValueError.
        assert isinstance(erro.value.orig, ValueError)

        # Confirma que a rejeição ocorreu pelo motivo esperado.
        assert (
            "A data deve conter informação de fuso horário."
            in str(erro.value.orig)
        )

        sessao.rollback()


def test_persistencia_utc_apos_nova_sessao(banco_teste):
    """Confirma o fuso UTC após reabrir uma sessão."""

    data_original = datetime(
        2026, 10, 30, 20, 30,
        tzinfo=timezone.utc,
    )

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Persistência UTC",
            criada_em=data_original,
        )

        sessao.add(atividade)
        sessao.commit()

        atividade_id = atividade.id

    with Session(banco_teste) as nova_sessao:
        recuperada = nova_sessao.get(
            Atividade,
            atividade_id,
        )

        assert recuperada is not None
        assert recuperada.criada_em == data_original
        assert recuperada.criada_em.utcoffset() == timedelta(0)