from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# =========================================================
# Base
# =========================================================
class EstudioBase(BaseModel):
    nome: str = Field(..., example="Studio Pilates Bela Vista")
    endereco: str = Field(..., example="Rua das Flores, 123 - Centro")
    cep: str = Field(..., example="12345-678", pattern=r"^\d{5}-\d{3}$")
    telefone: Optional[str] = Field(None, example="(11) 91234-5678")
    email: Optional[EmailStr] = Field(None, example="contato@studiopilates.com")
    capacidade_maxima: Optional[int] = Field(3, ge=1, example=5)

# =========================================================
# Create (Cadastro)
# =========================================================
class EstudioCreate(EstudioBase):
    pass

# =========================================================
# Update (Edição)
# =========================================================
class EstudioUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    cep: Optional[str] = Field(None, pattern=r"^\d{5}-\d{3}$")
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    capacidade_maxima: Optional[int] = Field(None, ge=1)

# =========================================================
# Response (Leitura / Retorno)
# =========================================================
class EstudioResponse(EstudioBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True
