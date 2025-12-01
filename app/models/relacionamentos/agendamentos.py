from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import Presenca

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)

    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    aula_id = Column(Integer, ForeignKey("agendas.id"), nullable=False)

    # Presença do aluno (indefinido, presente, ausente)
    presenca = Column(Enum(Presenca), default=Presenca.indefinido)

    aluno = relationship("Aluno", back_populates="agendamentos")
    agenda = relationship("Agenda", back_populates="agendamentos")


