import pytest

from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Categoria


@pytest.fixture
def banco_teste(tmp_path):
    """Cria um banco SQLite temporário para cada teste."""

    caminho = tmp_path / "teste_gat.db"

    engine = create_engine(
        f"sqlite:///{caminho.as_posix()}"
    )

    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()


def test_criar_categoria(banco_teste):
    """Verifica a criação de uma categoria."""

    with Session(banco_teste) as sessao:
        categoria = Categoria(
            nome="Estudos",
            cor="#3498db",
        )

        sessao.add(categoria)
        sessao.commit()

        assert categoria.id is not None
        assert categoria.nome == "Estudos"


def test_consultar_categoria(banco_teste):
    """Verifica a recuperação de uma categoria."""

    with Session(banco_teste) as sessao:
        categoria = Categoria(nome="Trabalho")

        sessao.add(categoria)
        sessao.commit()

    with Session(banco_teste) as sessao:
        resultado = sessao.scalar(
            select(Categoria).where(
                Categoria.nome == "Trabalho"
            )
        )

        assert resultado is not None
        assert resultado.nome == "Trabalho"


def test_categoria_nome_duplicado(banco_teste):
    """Impede nomes duplicados ignorando maiúsculas."""

    with Session(banco_teste) as sessao:
        sessao.add(Categoria(nome="Estudos"))
        sessao.commit()

        sessao.add(Categoria(nome="ESTUDOS"))

        with pytest.raises(IntegrityError):
            sessao.commit()

        sessao.rollback()


def test_categoria_ativa_por_padrao(banco_teste):
    """Verifica se uma nova categoria fica ativa."""

    with Session(banco_teste) as sessao:
        categoria = Categoria(nome="Pessoal")

        sessao.add(categoria)
        sessao.commit()
        sessao.refresh(categoria)

        assert categoria.ativa is True


def test_persistencia_apos_nova_sessao(banco_teste):
    """Verifica se os dados permanecem após fechar a sessão."""

    with Session(banco_teste) as sessao:
        categoria = Categoria(nome="Lazer")

        sessao.add(categoria)
        sessao.commit()

        categoria_id = categoria.id

    with Session(banco_teste) as nova_sessao:
        recuperada = nova_sessao.get(
            Categoria,
            categoria_id,
        )

        assert recuperada is not None
        assert recuperada.nome == "Lazer"