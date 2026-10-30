from sqlalchemy import text

from app.database import engine, verificar_conexao


def test_conexao_sqlite():
    assert verificar_conexao() is True


def test_consulta_sqlite():
    with engine.connect() as conexao:
        resultado = conexao.execute(text("SELECT 1"))

        assert resultado.scalar_one() == 1