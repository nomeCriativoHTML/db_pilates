from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import TipoIdentificador, StatusAula, Presenca

# ===========================
# PROFESSOR
# ===========================
class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cref = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    identificador = Column(String(100))
    tipo_identificador = Column(Enum(TipoIdentificador))
    ativo = Column(Boolean, default=True)
    estudio_id = Column(Integer, ForeignKey("estudios.id"), nullable=True)

    # Relacionamentos
    agendas = relationship(
        "Agenda",
        back_populates="professor",
        cascade="all, delete-orphan",
        foreign_keys="Agenda.professor_id"
    )

    #agendamentos = relationship("Agendamento", back_populates="professor")
    estudio = relationship("Estudio", back_populates="professores")
    evolucoes = relationship("MinhaEvolucao", back_populates="professor", cascade="all, delete-orphan")


# ===========================
# ALUNO NA AULA
# ===========================
class AlunoNaAula(Base):
    __tablename__ = "alunos_na_aula"

    id = Column(Integer, primary_key=True, index=True)
    agenda_id = Column(Integer, ForeignKey("agendas.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    presenca = Column(Enum(Presenca), default=Presenca.indefinido)
    observacoes = Column(String(255))

    agenda = relationship("Agenda", back_populates="alunos")
    aluno = relationship("Aluno")  # relacionamento com tabela principal Aluno
