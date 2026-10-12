from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Classe base que usaremos para transformar nossas classes Python em tabelas SQL
class Base(DeclarativeBase):
    pass

# Cria o motor do banco de dados. O arquivo "escola.db" será criado automaticamente.
# echo=False evita que o terminal fique poluído com os comandos SQL internos.
engine = create_engine("sqlite:///escola.db", echo=False)

# Cria a fábrica de sessões. É ela que usaremos para salvar, editar ou deletar dados.
SessionLocal = sessionmaker(bind=engine)