from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database.connection import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    user_type = Column(String(20), nullable=False)  # 'aluno', 'professor', 'admin'
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def is_valid(self):
        """Verifica se o token ainda é válido"""
        return datetime.utcnow() < self.expires_at and not self.used

    @classmethod
    def create_token(cls, email: str, user_type: str, expiration_hours: int = 24):
        """Cria um novo token de recuperação"""
        expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)
        # Gerar token seguro (será implementado no controller)
        return cls(
            email=email,
            token="",  # Será definido no controller
            user_type=user_type,
            expires_at=expires_at,
            used=False
        )