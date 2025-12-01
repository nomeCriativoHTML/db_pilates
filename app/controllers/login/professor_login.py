from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.professor import Professor
from app.utils.security import verify_senha, create_access_token
from app.schema.login.professor_login import ProfessorLogin

class ProfessorLoginController:

    @staticmethod
    def login_professor(db: Session, login_data: ProfessorLogin):
        # Buscar professor pelo e-mail
        professor = db.query(Professor).filter(Professor.email == login_data.email).first()

        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado."
            )

        # Verificar senha
        if not verify_senha(login_data.senha, professor.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Senha incorreta."
            )
        
         #  Gerar token JWT
        token = create_access_token({"sub": professor.email, "id": professor.id})
        
        # Verificar se professor está ativo
        if not professor.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta inativa. Contate o administrador."
            )

        return {
            "message": "Login realizado com sucesso!",
            "professor_id": professor.id,
            "nome": professor.nome,
            "token": token
        }


