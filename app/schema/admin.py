from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

# ====================================================
# ENUMS
# ====================================================

class TipoAdmin(str, Enum):
    pleno = "admin_pleno"
    recepcionista = "recepcionista"

class Status(str, Enum):
    ativo = "ativo"
    inativo = "inativo"
    pendente = "pendente"


# ====================================================
# ADMIN PRINCIPAL
# ====================================================

class AdminBase(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo_admin: TipoAdmin = TipoAdmin.recepcionista
    status: Optional[Status] = Status.ativo

class AdminCreate(AdminBase):
    pass

class AdminUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    tipo_admin: Optional[TipoAdmin] = None
    status: Optional[Status] = None

class AdminOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo_admin: TipoAdmin
    status: Status

    model_config = ConfigDict(from_attributes=True)


# ====================================================
# DASHBOARD
# ====================================================

class DashboardBase(BaseModel):
    total_alunos: int = 0
    total_professores: int = 0
    total_estudos: int = 0
    pagamentos_em_atraso: int = 0
    alunos_hide: int = 0
    professores_hide: int = 0
    ocupacao_media: Decimal = 0.0

class DashboardOut(DashboardBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ====================================================
# LOGS DO SISTEMA
# ====================================================

class LogsDoSistemaBase(BaseModel):
    usuario: str
    acao: str
    data_hora: datetime
    sistema_operacional: Optional[str] = None
    navegador: Optional[str] = None
    ip_address: Optional[str] = None

class LogsDoSistemaOut(LogsDoSistemaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ====================================================
# GESTÃO DE ESTUDOS
# ====================================================

class GestaoDeEstudosBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    tipo_estudo: str
    status: Optional[Status] = None
    carga_horaria: Optional[int] = 0
    total_professores: int = 0
    total_alunos: int = 0

class GestaoDeEstudosOut(GestaoDeEstudosBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ====================================================
# GESTÃO DE PROFESSORES
# ====================================================

class GestaoDeProfessoresBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    especialidade: Optional[str] = None
    status: Optional[Status] = None
    data_cadastro: Optional[date] = None
    total_estudos: int = 0
    total_alunos: int = 0

class GestaoDeProfessoresOut(GestaoDeProfessoresBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ====================================================
# GESTÃO DE ALUNOS
# ====================================================

class GestaoDeAlunosBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    status: Optional[Status] = None
    data_cadastro: Optional[date] = None
    total_estudos: int = 0
    total_professores: int = 0

class GestaoDeAlunosOut(GestaoDeAlunosBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ====================================================
# RELATÓRIOS DE EVOLUÇÃO
# ====================================================

class RelatoriosDeEvolucaoBase(BaseModel):
    nome: str
    data_criacao: date
    total_estudos: int = 0
    total_professores: int = 0
    total_alunos: int = 0
    alunos_ativos: int = 0

class RelatoriosDeEvolucaoOut(RelatoriosDeEvolucaoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ====================================================
# RELATÓRIOS FINANCEIROS
# ====================================================

class RelatoriosFinanceirosBase(BaseModel):
    nome: str
    data_criacao: date
    total_alunos: int = 0
    alunos_pagantes: int = 0
    alunos_inadimplentes: int = 0
    taxa_ocupacao: Decimal = 0.0

class RelatoriosFinanceirosOut(RelatoriosFinanceirosBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
