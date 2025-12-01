from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional, List

# --- Enums ---
class TipoIdentificador(str, Enum):
    cpf = "cpf"
    rg = "rg"
    outro = "outro"

class StatusAula(str, Enum):
    disponivel = "disponivel"
    em_andamento = "em_andamento"
    finalizada = "finalizada"

class Presenca(str, Enum):
    presente = "presente"
    ausente = "ausente"
    indefinido = "indefinido"

# --- Professor ---
class ProfessorBase(BaseModel):
    nome: str
    cref: str 
    email: EmailStr
    senha: str
    identificador: Optional[str] = None
    tipo_identificador: Optional[TipoIdentificador] = None
    ativo: Optional[bool] = True
    estudio_id: Optional[int] = None 

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    cref: Optional[str] = None  
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    identificador: Optional[str] = None
    tipo_identificador: Optional[TipoIdentificador] = None
    ativo: Optional[bool] = None
    estudio_id: Optional[int] = None 

class ProfessorOut(ProfessorBase):
    id: int

    class Config:
        orm_mode = True

# --- Agenda ---
class AgendaBase(BaseModel):
    professor_id: int
    data_hora: datetime
    tipo_aula: str
    estudo: str
    alunos_confirmados: Optional[int] = 0
    max_alunos: Optional[int] = 3
    status: Optional[StatusAula] = StatusAula.disponivel

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(BaseModel):
    data_hora: Optional[datetime] = None
    tipo_aula: Optional[str] = None
    estudo: Optional[str] = None
    alunos_confirmados: Optional[int] = None
    max_alunos: Optional[int] = None
    status: Optional[StatusAula] = None

class AgendaOut(AgendaBase):
    id: int

    class Config:
        orm_mode = True

# --- AlunoNaAula ---
class AlunoNaAulaBase(BaseModel):
    agenda_id: int
    aluno_nome: str
    presenca: Optional[Presenca] = Presenca.indefinido
    observacoes: Optional[str] = None

class AlunoNaAulaCreate(AlunoNaAulaBase):
    pass

class AlunoNaAulaUpdate(BaseModel):
    presenca: Optional[Presenca] = None
    observacoes: Optional[str] = None

class AlunoNaAulaOut(AlunoNaAulaBase):
    id: int

    class Config:
        orm_mode = True

# --- DadosAluno ---
class DadosAlunoBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    restricoes: Optional[str] = None
    interesses: Optional[str] = None
    evolucao: Optional[str] = None

class DadosAlunoCreate(DadosAlunoBase):
    pass

class DadosAlunoUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    restricoes: Optional[str] = None
    interesses: Optional[str] = None
    evolucao: Optional[str] = None

class DadosAlunoOut(DadosAlunoBase):
    id: int

    class Config:
        orm_mode = True
