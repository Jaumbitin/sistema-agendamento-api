# Sistema de Agendamento API

Protótipo de API para cadastrar professores e alunos, criar aulas e realizar matrículas, usando **FastAPI, SQLAlchemy e SQLite**.

## Estado atual

As rotas estão em `api.py`. O login verifica a senha e retorna dados do usuário, mas **não emite token nem cria uma sessão autenticada**. As rotas de cadastro, criação de aula e matrícula não verificam autenticação ou permissões. Use apenas dados fictícios em ambiente local enquanto essa proteção não estiver implementada.

O arquivo `main.py` referencia `views.telas`, que não está no repositório. Ele não é o ponto de entrada funcional da API.

## Requisitos

O `pyproject.toml` declara **Python >= 3.15** e dependências de FastAPI, SQLAlchemy, Uvicorn e Werkzeug. Use uma versão compatível com essa declaração. O `uv.lock` está incluído para instalação com uv.

## Executar localmente com uv

```powershell
git clone https://github.com/Jaumbitin/sistema-agendamento-api.git
cd sistema-agendamento-api
uv sync --frozen
uv run python -c "from database.config import Base, engine; import models.entidades; Base.metadata.create_all(bind=engine)"
uv run uvicorn api:app --host 127.0.0.1 --port 8000
```

Acesse a documentação interativa em [localhost:8000/docs](http://localhost:8000/docs). O comando de criação de tabelas prepara um banco novo, sem depender do `main.py`.

## Endpoints

| Método | Rota | Função |
|---|---|---|
| GET | / | Mensagem de disponibilidade |
| POST | /login | Confere e-mail e senha; retorna id, nome e papel |
| POST | /professores | Cadastra professor |
| POST | /alunos | Cadastra aluno |
| POST | /aulas | Cria aula para um professor |
| GET | /aulas | Lista aulas |
| POST | /matricular | Vincula aluno e aula |

Os formatos dos corpos JSON podem ser consultados em `/docs`. O cadastro usa hashes gerados pelo Werkzeug; não devolve o hash nas respostas da API.

## Estrutura

- `api.py`: rotas e modelos de entrada.
- `controllers/sistema.py`: operações de cadastro, login, aulas e matrículas.
- `models/entidades.py`: usuários, herança de papéis e relacionamentos.
- `database/config.py`: conexão SQLite e fábrica de sessões.
- `pyproject.toml` e `uv.lock`: dependências.

## Pendências de segurança e manutenção

- O `escola.db` publicado contém registros de usuários e hashes de senha. Trate como dados potencialmente expostos; não reutilize essas credenciais. Remover o arquivo atual não apaga o histórico.
- `.gitignore.txt` não funciona como `.gitignore`. Corrigir o nome e deixar de versionar banco, `__pycache__/` e configurações locais exige uma alteração própria no Git.
- Implementar autenticação, autorização por papel e controle de quem pode matricular cada aluno.
- Encerrar as sessões SQLAlchemy em todos os fluxos.
- Adicionar testes automatizados; não há suíte de testes publicada.

Esta documentação descreve as limitações existentes; não implementa essas correções.
