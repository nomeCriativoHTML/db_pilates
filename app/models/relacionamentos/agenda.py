from sqlalchemy import Column, Integer, Date, Time, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import StatusAula

class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(Integer, primary_key=True, index=True)

    # Estúdio onde a aula ocorre
    estudio_id = Column(Integer, ForeignKey("estudios.id"), nullable=False)

    # Professor responsável (fixo)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)

    # Substituto (caso o professor falte ou esteja de férias)
    substituto_id = Column(Integer, ForeignKey("professores.id"), nullable=True)

    # Data do dia da aula
    data = Column(Date, nullable=False)

    # Horário específico
    hora = Column(Time, nullable=False)

    # Se é aula normal, experimental, particular etc
    tipo_aula = Column(String(50))

    # Limite de alunos (por padrão 3)
    max_alunos = Column(Integer, default=3)

    # Status da aula (disponível, em andamento, finalizada, cancelada)
    status = Column(Enum(StatusAula), default=StatusAula.disponivel)

    # Bloqueios (feriados, manutenção, recessos)
    bloqueado = Column(Boolean, default=False)
    motivo_bloqueio = Column(String(255))

    # Relacionamentos
    estudio = relationship("Estudio", back_populates="agendas")
    professor = relationship("Professor", foreign_keys=[professor_id], back_populates="agendas")
    substituto = relationship("Professor", foreign_keys=[substituto_id])

    # Lista de alunos agendados
    agendamentos = relationship("Agendamento", back_populates="agenda", cascade="all, delete-orphan")

    # Alunos efetivamente presentes (separada da reserva)
    alunos = relationship("AlunoNaAula", back_populates="agenda", cascade="all, delete-orphan")

    # Evoluções
    evolucoes = relationship("MinhaEvolucao", back_populates="agenda", cascade="all, delete-orphan")
