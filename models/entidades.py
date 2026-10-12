from typing import List
from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importando a Base do nosso arquivo config.py
from database.config import Base

# Tabela auxiliar para a relação "Muitos para Muitos" entre Aluno e Aula
aula_aluno = Table(
    "aula_aluno",
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("usuarios.id"), primary_key=True),
    Column("aula_id", Integer, ForeignKey("aulas.id"), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(100))
    papel: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_on": "papel",
        "polymorphic_identity": "USUARIO"
    }

class Professor(Usuario):
    __mapper_args__ = {"polymorphic_identity": "PROFESSOR"}

    aulas_ministradas: Mapped[List["Aula"]] = relationship(back_populates="professor")

class Aluno(Usuario):
    __mapper_args__ = {"polymorphic_identity": "ALUNO"}

    aulas_matriculadas: Mapped[List["Aula"]] = relationship(
        secondary=aula_aluno, back_populates="alunos_matriculados"
    )

class Aula(Base):
    __tablename__ = "aulas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    horario: Mapped[str] = mapped_column(String(50))
    professor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    professor: Mapped["Professor"] = relationship(back_populates="aulas_ministradas")
    alunos_matriculados: Mapped[List["Aluno"]] = relationship(
        secondary=aula_aluno, back_populates="aulas_matriculadas"
    )