from sqlalchemy import Column, Integer, String, DateTime, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base  


class Estudio(Base):
    __tablename__ = "estudios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(255), nullable=False)
    cep = Column(String(9), nullable=False)  
    telefone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    capacidade_maxima = Column(Integer, default=3)
    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    agendas = relationship("Agenda", back_populates="estudio", cascade="all, delete-orphan")
    professores = relationship("Professor", back_populates="estudio")

    # Horários de funcionamento do estúdio
    horarios = relationship(
        "HorarioFuncionamento",
        back_populates="estudio",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Estudio(nome='{self.nome}', cep='{self.cep}', capacidade={self.capacidade_maxima})>"


# ================================
# HORÁRIOS DE FUNCIONAMENTO
# ================================
class HorarioFuncionamento(Base):
    __tablename__ = "horarios_funcionamento"

    id = Column(Integer, primary_key=True)
    estudio_id = Column(Integer, ForeignKey("estudios.id"), nullable=False)
    dia_semana = Column(String(15), nullable=False)  # segunda, terça, quarta...
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    # Relacionamento reverso
    estudio = relationship("Estudio", back_populates="horarios")
