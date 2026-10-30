from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Diretório principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretório de armazenamento
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Caminho do banco de dados
DATABASE_PATH = DATA_DIR / "gat.db"

# URL de conexão SQLite
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Mecanismo de conexão
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Fábrica de sessões
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# Classe-base para os futuros modelos
class Base(DeclarativeBase):
    pass


# Verificação da conexão
def verificar_conexao():
    with engine.connect() as conexao:
        resultado = conexao.execute(text("SELECT 1"))
        return resultado.scalar_one() == 1