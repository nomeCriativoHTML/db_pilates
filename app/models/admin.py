from sqlalchemy import Column, Integer, String, Date, DateTime, DECIMAL, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.enums import Status, TipoAdmin

# ===========================
# ADMIN
# ===========================
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    tipo_admin = Column(String(30), nullable=False, default="recepcionista")
    ativo = Column(Boolean, default=True)


    # Relacionamentos
    logs = relationship("LogDoSistema", back_populates="admin", cascade="all, delete-orphan")


# ===========================
# LOGS DO SISTEMA
# ===========================
class LogDoSistema(Base):
    __tablename__ = "logs_do_sistema"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)
    acao = Column(String(255))
    data_hora = Column(DateTime)
    sistema_operacional = Column(String(50))
    navegador = Column(String(50))
    ip_address = Column(String(45))

    admin = relationship("Admin", back_populates="logs")


# ===========================
# DASHBOARD (Métricas)
# ===========================
class Dashboard(Base):
    __tablename__ = "dashboards"

    id = Column(Integer, primary_key=True, index=True)
    total_alunos = Column(Integer, default=0)
    total_professores = Column(Integer, default=0)
    total_estudos = Column(Integer, default=0)
    pagamentos_em_atraso = Column(Integer, default=0)
    ocupacao_media = Column(DECIMAL(5, 2), default=0.0)
