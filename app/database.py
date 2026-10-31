from pathlib import Path

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "gat.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def ativar_chaves_estrangeiras(dbapi_connection, connection_record):
    """Ativa a integridade referencial em cada conexão SQLite."""

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def verificar_conexao():
    """Verifica se a conexão com o SQLite está funcionando."""

    with engine.connect() as conexao:
        resultado = conexao.execute(text("SELECT 1"))

        return resultado.scalar_one() == 1