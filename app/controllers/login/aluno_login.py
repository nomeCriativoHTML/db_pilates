
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.aluno import Aluno
from app.schema.login.aluno_login import AlunoLogin
from app.utils.security import verify_senha, create_access_token


class AlunoLoginController:

    @staticmethod
    def login_aluno(db: Session, dados: AlunoLogin):
        # Buscar aluno
        aluno = db.query(Aluno).filter(Aluno.email == dados.email).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )

        # Verificar senha
        if not verify_senha(dados.senha, aluno.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Senha incorreta."
            )

        # Gerar token JWT
        token = create_access_token({"sub": aluno.email, "id": aluno.id})

        # Retorno padronizado com o login de professor
        return {
            "message": "Login realizado com sucesso!",
            "aluno_id": aluno.id,
            "nome": aluno.nome,
            "token": token
        }
