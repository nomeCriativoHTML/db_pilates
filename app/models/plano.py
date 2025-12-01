# app/models/plano.py
from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base

class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    periodo = Column(String(20), nullable=False)      # mensal, trimestral, etc
    frequencia = Column(Integer, nullable=False)      # 1, 2 ou 3 vezes na semana
    valor_mensal = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
    politica_cancelamento = Column(String(255), nullable=True)
