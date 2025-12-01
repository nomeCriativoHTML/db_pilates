from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.admin import Admin
from app.utils.security import verify_senha, create_access_token
from app.schema.login.admin_login import AdminLogin


class AdminLoginController:

    @staticmethod
    def login_admin(db: Session, dados: AdminLogin):
        admin = db.query(Admin).filter(Admin.email == dados.email).first()

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="E-mail não cadastrado como administrador."
            )

        if not verify_senha(dados.senha, admin.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Senha incorreta."
            )
        
         #  Gerar token JWT
        token = create_access_token({"sub": admin.email, "id": admin.id})

        if not admin.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta de administrador inativa."
            )

        return {
            "mensagem": f"Bem-vindo(a), {admin.nome}!",
            "admin_id": admin.id,
            "tipo_admin": admin.tipo_admin,
            "token": token
        }
