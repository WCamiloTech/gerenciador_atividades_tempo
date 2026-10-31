
from datetime import datetime, timedelta, timezone

import pytest

from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Atividade, SessaoTempo


@pytest.fixture
def banco_teste(tmp_path):
    """Cria um banco temporário com chaves estrangeiras ativas."""

    caminho = tmp_path / "teste_sessoes.db"

    engine = create_engine(
        f"sqlite:///{caminho.as_posix()}"
    )

    @event.listens_for(engine, "connect")
    def ativar_chaves_estrangeiras(
        dbapi_connection,
        connection_record,
    ):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()


def criar_atividade(sessao, titulo="Estudo"):
    """Cria uma atividade para os testes."""

    atividade = Atividade(titulo=titulo)

    sessao.add(atividade)
    sessao.flush()

    return atividade


def test_iniciar_sessao(banco_teste):
    """Uma sessão pode começar sem horário de término."""

    with Session(banco_teste) as sessao:
        atividade = criar_atividade(sessao)

        registro = SessaoTempo(
            atividade_id=atividade.id,
            inicio_em=datetime.now(timezone.utc),
        )

        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)

        assert registro.id is not None
        assert registro.fim_em is None
        assert registro.inicio_em.tzinfo == timezone.utc


def test_encerrar_sessao_e_calcular_duracao(banco_teste):
    """O tempo decorrido é calculado a partir dos horários."""

    inicio = datetime(
        2026, 10, 30, 9, 0,
        tzinfo=timezone.utc,
    )

    fim = inicio + timedelta(hours=1, minutes=30)

    with Session(banco_teste) as sessao:
        atividade = criar_atividade(sessao)

        registro = SessaoTempo(
            atividade_id=atividade.id,
            inicio_em=inicio,
        )

        sessao.add(registro)
        sessao.flush()

        registro.fim_em = fim

        sessao.commit()
        sessao.refresh(registro)

        duracao = registro.fim_em - registro.inicio_em

        assert duracao == timedelta(hours=1, minutes=30)


def test_impedir_duas_sessoes_abertas(banco_teste):
    """Uma atividade não pode possuir duas sessões abertas."""

    with Session(banco_teste) as sessao:
        atividade = criar_atividade(sessao)

        primeira = SessaoTempo(
            atividade_id=atividade.id,
            inicio_em=datetime.now(timezone.utc),
        )

        sessao.add(primeira)
        sessao.commit()

        segunda = SessaoTempo(
            atividade_id=atividade.id,
            inicio_em=datetime.now(timezone.utc),
        )

        sessao.add(segunda)

        with pytest.raises(IntegrityError):
            sessao.commit()

        sessao.rollback()


def test_sessoes_simultaneas_atividades_diferentes(banco_teste):
    """Atividades diferentes podem ter sessões abertas."""

    inicio = datetime.now(timezone.utc)

    with Session(banco_teste) as sessao:
        atividade_a = criar_atividade(sessao, "Estudo")
        atividade_b = criar_atividade(sessao, "Trabalho")

        registro_a = SessaoTempo(
            atividade_id=atividade_a.id,
            inicio_em=inicio,
        )

        registro_b = SessaoTempo(
            atividade_id=atividade_b.id,
            inicio_em=inicio,
        )

        sessao.add_all([registro_a, registro_b])
        sessao.commit()

        assert registro_a.fim_em is None
        assert registro_b.fim_em is None
        assert registro_a.id != registro_b.id


def test_rejeitar_termino_anterior_inicio(banco_teste):
    """O banco rejeita sessões com término anterior ao início."""

    inicio = datetime(
        2026, 10, 30, 12, 0,
        tzinfo=timezone.utc,
    )

    fim = inicio - timedelta(minutes=30)

    with Session(banco_teste) as sessao:
        atividade = criar_atividade(sessao)

        registro = SessaoTempo(
            atividade_id=atividade.id,
            inicio_em=inicio,
            fim_em=fim,
        )

        sessao.add(registro)

        with pytest.raises(IntegrityError):
            sessao.commit()

        sessao.rollback()
