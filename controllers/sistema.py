# controllers/sistema.py
from database.config import SessionLocal
from models.entidades import Usuario, Professor, Aluno, Aula
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


def autenticar_usuario(email, senha):
    session = SessionLocal()
    usuario = session.query(Usuario).filter_by(email=email).first()
    if usuario and check_password_hash(usuario.senha_hash, senha):
        return usuario
    return None


def cadastrar_professor(nome, email, senha):
    session = SessionLocal()
    try:
        senha_hash = generate_password_hash(senha)
        novo_prof = Professor(nome=nome, email=email, senha_hash=senha_hash)
        session.add(novo_prof)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def cadastrar_aluno(nome, email, senha):
    session = SessionLocal()
    try:
        senha_hash = generate_password_hash(senha)
        novo_aluno = Aluno(nome=nome, email=email, senha_hash=senha_hash)
        session.add(novo_aluno)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def criar_aula(titulo, horario, professor_id):
    session = SessionLocal()
    professor = session.query(Professor).filter_by(id=professor_id).first()
    if professor:
        nova_aula = Aula(titulo=titulo, horario=horario, professor=professor)
        session.add(nova_aula)
        session.commit()
        return True
    return False


def listar_todas_aulas():
    """ Retorna uma lista com todas as aulas do banco """
    session = SessionLocal()
    return session.query(Aula).all()


def matricular_aluno_na_aula(aluno_id, aula_id):
    """ Conecta o aluno à aula na tabela associativa """
    session = SessionLocal()
    aluno = session.query(Aluno).filter_by(id=aluno_id).first()
    aula = session.query(Aula).filter_by(id=aula_id).first()

    if aluno and aula:
        if aluno not in aula.alunos_matriculados:
            aula.alunos_matriculados.append(aluno)
            session.commit()
            return "SUCESSO"
        return "JA_MATRICULADO"
    return "ERRO"
def listar_aulas_do_aluno(aluno_id):
    """ Retorna todas as aulas em que este aluno específico está matriculado """
    session = SessionLocal()
    aluno = session.query(Aluno).filter_by(id=aluno_id).first()
    if aluno:
        # O SQLAlchemy preenche essa lista automaticamente através da tabela associativa
        return aluno.aulas_matriculadas
    return []