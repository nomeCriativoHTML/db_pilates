import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.password_reset import PasswordResetToken
from app.models.aluno import Aluno
from app.models.professor import Professor
from app.models.admin import Admin
from app.schema.login.password_reset import (
    PasswordResetRequest, 
    PasswordResetConfirm,
    PasswordResetVerify
)
from app.utils.security import hash_senha
# from app.utils.email_service import send_password_reset_email

class PasswordResetController:

    @staticmethod
    def request_password_reset(db: Session, request: PasswordResetRequest):
        """Solicita recuperação de senha e envia email"""
        
        # Verificar se o usuário existe
        user = PasswordResetController._get_user_by_type_and_email(
            db, request.user_type, request.email
        )
        if not user:
            # Por segurança, não revelamos se o email existe ou não
            return {
                "message": "Se o email existir em nosso sistema, enviaremos instruções de recuperação",
                "success": True
            }

        # Invalidar tokens anteriores do mesmo usuário
        db.query(PasswordResetToken).filter(
            PasswordResetToken.email == request.email,
            PasswordResetToken.user_type == request.user_type,
            PasswordResetToken.used == False
        ).update({"used": True})

        # Gerar token seguro
        token = secrets.token_urlsafe(32)
        
        # Criar novo token de recuperação
        reset_token = PasswordResetToken(
            email=request.email,
            token=token,
            user_type=request.user_type,
            expires_at=datetime.utcnow() + timedelta(hours=24),
            used=False
        )

        db.add(reset_token)
        db.commit()
        db.refresh(reset_token)

        # Enviar email (implementaremos depois)
        try:
            # send_password_reset_email(request.email, token, request.user_type)
            print(f"Token de recuperação para {request.email}: {token}")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")

        return {
            "message": "Se o email existir em nosso sistema, enviaremos instruções de recuperação",
            "success": True,
            "token": token  # Apenas para desenvolvimento
        }

    @staticmethod
    def verify_token(db: Session, verify: PasswordResetVerify):
        """Verifica se um token é válido"""
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == verify.token,
            PasswordResetToken.email == verify.email
        ).first()

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token inválido ou expirado"
            )

        if token_record.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token já utilizado"
            )

        if datetime.utcnow() > token_record.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token expirado"
            )

        return {
            "message": "Token válido",
            "success": True,
            "email": token_record.email,
            "user_type": token_record.user_type
        }

    @staticmethod
    def reset_password(db: Session, confirm: PasswordResetConfirm):
        """Redefine a senha do usuário"""
        
        # Verificar token
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == confirm.token,
            PasswordResetToken.email == confirm.email
        ).first()

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token inválido"
            )

        if token_record.used:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token já utilizado"
            )

        if datetime.utcnow() > token_record.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token expirado"
            )

        # Buscar usuário
        user = PasswordResetController._get_user_by_type_and_email(
            db, token_record.user_type, token_record.email
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        # Atualizar senha
        user.senha = hash_senha(confirm.new_password)
        
        # Marcar token como usado
        token_record.used = True
        token_record.expires_at = datetime.utcnow()  # Expira imediatamente

        db.commit()

        return {
            "message": "Senha redefinida com sucesso",
            "success": True
        }

    @staticmethod
    def _get_user_by_type_and_email(db: Session, user_type: str, email: str):
        """Busca usuário pelo tipo e email"""
        if user_type == 'aluno':
            return db.query(Aluno).filter(Aluno.email == email).first()
        elif user_type == 'professor':
            return db.query(Professor).filter(Professor.email == email).first()
        elif user_type == 'admin':
            return db.query(Admin).filter(Admin.email == email).first()
        return None