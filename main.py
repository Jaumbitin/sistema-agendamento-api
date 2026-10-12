# main.py
from database.config import engine, Base
from views.telas import exibir_menu_principal

# Importar os models para o SQLAlchemy criar as tabelas
from models.entidades import Usuario

def iniciar_sistema():
    Base.metadata.create_all(bind=engine)
    exibir_menu_principal()

if __name__ == "__main__":
    iniciar_sistema()