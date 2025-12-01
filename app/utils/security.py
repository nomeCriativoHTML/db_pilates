import hashlib
import jwt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.professor import Professor
from app.models.aluno import Aluno
from app.models.admin import Admin


SECRET_KEY = "sua_chave_secreta_aqui"  # mudar para uma variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # duração do token JWT

# -------------------------------
# Funções de hash de senha
# -------------------------------
def hash_senha(senha: str) -> str:
    """Criptografa a senha usando SHA-256."""
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def verify_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return hash_senha(senha) == senha_hash

# -------------------------------
# Função para criar JWT
# -------------------------------
def create_access_token(data: dict) -> str:
    """Gera um token JWT com payload."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token





def get_current_professor(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("professor_access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        professor_id: int = payload.get("id")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    professor = db.query(Professor).filter(Professor.id == professor_id).first()

    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    return professor


def get_current_aluno(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("aluno_access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        aluno_id: int = payload.get("id")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return aluno



def get_current_admin(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("admin_access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_id: int = payload.get("id")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")

    return admin