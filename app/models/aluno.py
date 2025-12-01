from sqlalchemy import Column, Integer, String, Date, DateTime, Text, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import StatusPagamento, Presenca

# ===========================
# ALUNO
# ===========================
class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20))
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)
    data_nascimento = Column(Date)
    status_pagamento = Column(
        Enum(StatusPagamento, name="status_pagamento_enum"),
        default=StatusPagamento.pendente,
        nullable=False
    )

    # Relacionamentos
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=True)

    plano = relationship("Plano")
    evolucoes = relationship("MinhaEvolucao", back_populates="aluno", cascade="all, delete-orphan")
    pagamentos = relationship("MeusPagamentos", back_populates="aluno", cascade="all, delete-orphan")
    agendamentos = relationship("Agendamento", back_populates="aluno")



# ===========================
# MINHA EVOLUÇÃO
# ===========================
class MinhaEvolucao(Base):
    __tablename__ = "minha_evolucao"

    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    agenda_id = Column(Integer, ForeignKey("agendas.id"), nullable=False)
    data_aula = Column(DateTime, nullable=False)
    exercicios_realizados = Column(Text)
    observacoes = Column(Text)
    progresso = Column(String(50))

    aluno = relationship("Aluno", back_populates="evolucoes")
    professor = relationship("Professor", back_populates="evolucoes")  # precisa existir back_populates na Professor
    agenda = relationship("Agenda", back_populates="evolucoes")      # precisa existir back_populates na Agenda


# ===========================
# MEUS PAGAMENTOS
# ===========================
class MeusPagamentos(Base):
    __tablename__ = "meus_pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    data_pagamento = Column(Date, nullable=False)
    status_pagamento = Column(
        Enum(StatusPagamento, name="status_pagamento_enum"),
        default=StatusPagamento.pendente,
        nullable=False
    )
    metodo_pagamento = Column(String(50), nullable=False)

    aluno = relationship("Aluno", back_populates="pagamentos")


