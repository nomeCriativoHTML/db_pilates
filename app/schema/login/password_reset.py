from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class PasswordResetRequest(BaseModel):
    email: EmailStr
    user_type: str  # 'aluno', 'professor', 'admin'

    @validator('user_type')
    def validate_user_type(cls, v):
        if v not in ['aluno', 'professor', 'admin']:
            raise ValueError('Tipo de usuário deve ser: aluno, professor ou admin')
        return v

class PasswordResetVerify(BaseModel):
    token: str
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    email: EmailStr
    new_password: str
    confirm_password: str

    @validator('new_password')
    def validate_password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres')
        # Adicione mais validações de força de senha se desejar
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('As senhas não coincidem')
        return v

class PasswordResetResponse(BaseModel):
    message: str
    success: bool
    token: Optional[str] = None

class PasswordResetError(BaseModel):
    error: str
    success: bool = False