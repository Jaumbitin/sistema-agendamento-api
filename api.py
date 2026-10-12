# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importa as regras de negócio prontas da nossa pasta controllers
from controllers.sistema import (
    autenticar_usuario,
    cadastrar_professor,
    cadastrar_aluno,
    criar_aula,
    listar_todas_aulas,
    matricular_aluno_na_aula
)

app = FastAPI(title="Sistema de Agendamento - API", version="1.0")

# Classes Pydantic servem para validar os dados que chegam via JSON na web
class UsuarioLogin(BaseModel):
    email: str
    senha: str

class ProfessorCreate(BaseModel):
    nome: str
    email: str
    senha: str

class AlunoCreate(BaseModel):
    nome: str
    email: str
    senha: str

class AulaCreate(BaseModel):
    titulo: str
    horario: str
    professor_id: int

class MatriculaCreate(BaseModel):
    aluno_id: int
    aula_id: int

@app.get("/")
def home():
    return {"mensagem": "API do Sistema de Agendamento rodando com sucesso! Acesse /docs"}

@app.post("/login")
def login(dados: UsuarioLogin):
    usuario = autenticar_usuario(dados.email, dados.senha)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos.")
    return {
        "mensagem": f"Bem-vindo, {usuario.nome}!",
        "id": usuario.id,
        "nome": usuario.nome,
        "papel": usuario.papel
    }

@app.post("/professores")
def criar_professor(dados: ProfessorCreate):
    sucesso = cadastrar_professor(dados.nome, dados.email, dados.senha)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro: Email já cadastrado.")
    return {"mensagem": "Professor cadastrado com sucesso!"}

@app.post("/alunos")
def criar_aluno(dados: AlunoCreate):
    sucesso = cadastrar_aluno(dados.nome, dados.email, dados.senha)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro: Email já cadastrado.")
    return {"mensagem": "Aluno cadastrado com sucesso!"}

@app.post("/aulas")
def nova_aula(dados: AulaCreate):
    sucesso = criar_aula(dados.titulo, dados.horario, dados.professor_id)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Professor não encontrado.")
    return {"mensagem": "Aula criada com sucesso!"}

@app.get("/aulas")
def listar_aulas():
    aulas = listar_todas_aulas()
    # Converte os objetos do banco em dicionários simples para a web
    return [
        {
            "id": a.id,
            "titulo": a.titulo,
            "horario": a.horario,
            "professor": a.professor.nome if a.professor else "Desconhecido"
        }
        for a in aulas
    ]

@app.post("/matricular")
def matricular(dados: MatriculaCreate):
    resultado = matricular_aluno_na_aula(dados.aluno_id, dados.aula_id)
    if resultado == "SUCESSO":
        return {"mensagem": "Matrícula realizada com sucesso!"}
    elif resultado == "JA_MATRICULADO":
        raise HTTPException(status_code=400, detail="Aluno já está matriculado nesta aula.")
    else:
        raise HTTPException(status_code=404, detail="Aluno ou aula não encontrados.")