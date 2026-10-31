import pytest

from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Atividade, Categoria


@pytest.fixture
def banco_teste(tmp_path):
    """Cria um banco SQLite temporário com integridade referencial."""

    caminho = tmp_path / "teste_atividades.db"

    engine = create_engine(
        f"sqlite:///{caminho.as_posix()}"
    )

    @event.listens_for(engine, "connect")
    def ativar_chaves_estrangeiras(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()


def test_criar_atividade(banco_teste):
    """Verifica o cadastro de uma atividade."""

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Estudo",
            descricao="Estudando Python",
        )

        sessao.add(atividade)
        sessao.commit()
        sessao.refresh(atividade)

        assert atividade.id is not None
        assert atividade.titulo == "Estudo"
        assert atividade.descricao == "Estudando Python"


def test_atividade_valores_padrao(banco_teste):
    """Verifica os valores padrão da atividade."""

    with Session(banco_teste) as sessao:
        atividade = Atividade(titulo="Leitura")

        sessao.add(atividade)
        sessao.commit()
        sessao.refresh(atividade)

        assert atividade.status == "em_andamento"
        assert atividade.origem == "espontanea"
        assert atividade.criada_em is not None
        assert atividade.atualizada_em is not None


def test_atividade_com_categoria(banco_teste):
    """Verifica a associação com uma categoria existente."""

    with Session(banco_teste) as sessao:
        categoria = Categoria(nome="Estudos")

        sessao.add(categoria)
        sessao.flush()

        atividade = Atividade(
            titulo="Estudar Python",
            categoria_id=categoria.id,
        )

        sessao.add(atividade)
        sessao.commit()

        atividade_id = atividade.id
        categoria_id = categoria.id

    with Session(banco_teste) as sessao:
        recuperada = sessao.get(Atividade, atividade_id)

        assert recuperada is not None
        assert recuperada.categoria_id == categoria_id


def test_atividade_categoria_inexistente(banco_teste):
    """Impede associar uma atividade a uma categoria inexistente."""

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Atividade inválida",
            categoria_id="00000000-0000-0000-0000-000000000000",
        )

        sessao.add(atividade)

        with pytest.raises(IntegrityError):
            sessao.commit()

        sessao.rollback()


def test_persistencia_atividade(banco_teste):
    """Verifica a persistência após encerrar uma sessão."""

    with Session(banco_teste) as sessao:
        atividade = Atividade(
            titulo="Trabalho",
            descricao="Organização de documentos",
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
        assert recuperada.titulo == "Trabalho"


def test_exclusao_logica(banco_teste):
    """Verifica a marcação de exclusão lógica."""

    from datetime import datetime, timezone

    with Session(banco_teste) as sessao:
        atividade = Atividade(titulo="Atividade temporária")

        sessao.add(atividade)
        sessao.commit()

        atividade.excluida_em = datetime.now(timezone.utc)
        sessao.commit()

        atividade_id = atividade.id

    with Session(banco_teste) as sessao:
        recuperada = sessao.get(Atividade, atividade_id)

        assert recuperada is not None
        assert recuperada.excluida_em is not None