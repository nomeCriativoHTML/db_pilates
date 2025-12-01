from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from datetime import date, datetime
from typing import Optional, List

# ===========================
# ENUMS
# ===========================
class StatusPagamento(str, Enum):
    pendente = "pendente"
    pago = "pago"
    atrasado = "atrasado"

class Presenca(str, Enum):
    presente = "presente"
    ausente = "ausente"
    indefinido = "indefinido"

# ===========================
# MINHA EVOLUÇÃO
# ===========================
class MinhaEvolucaoBase(BaseModel):
    data_aula: datetime
    professor_id: int
    agenda_id: int
    exercicios_realizados: Optional[str] = None
    observacoes: Optional[str] = None
    progresso: Optional[str] = None

class MinhaEvolucaoCreate(MinhaEvolucaoBase):
    pass

class MinhaEvolucaoUpdate(MinhaEvolucaoBase):
    pass

class MinhaEvolucaoOut(MinhaEvolucaoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ===========================
# MEUS PAGAMENTOS
# ===========================
class MeusPagamentosBase(BaseModel):
    valor: float
    data_pagamento: date
    status_pagamento: Optional[StatusPagamento] = StatusPagamento.pendente
    metodo_pagamento: str

class MeusPagamentosCreate(MeusPagamentosBase):
    pass

class MeusPagamentosUpdate(MeusPagamentosBase):
    pass

class MeusPagamentosOut(MeusPagamentosBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ===========================
# AGENDAMENTOS
# ===========================
class AgendamentoBase(BaseModel):
    professor_id: int
    aula_id: int
    data_hora: datetime
    minha_presenca: Optional[Presenca] = Presenca.indefinido

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(AgendamentoBase):
    pass

class AgendamentoOut(AgendamentoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ===========================
# ALUNO
# ===========================
class AlunoBase(BaseModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    email: EmailStr
    senha: str
    data_nascimento: Optional[date] = None
    status_pagamento: StatusPagamento = StatusPagamento.pendente

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    data_nascimento: Optional[date] = None
    status_pagamento: Optional[StatusPagamento] = None

class AlunoOut(AlunoBase):
    id: int
    evolucoes: List[MinhaEvolucaoOut] = []
    pagamentos: List[MeusPagamentosOut] = []
    agendamentos: List[AgendamentoOut] = []

    model_config = ConfigDict(from_attributes=True)
