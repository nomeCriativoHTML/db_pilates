from pydantic import BaseModel
from typing import Optional


class PlanoBase(BaseModel):
    periodo: Optional[str] = None
    frequencia: Optional[int] = None
    valor_mensal: Optional[float] = None
    valor_total: Optional[float] = None
    politica_cancelamento: Optional[str] = None


class PlanoCreate(PlanoBase):
    periodo: str
    frequencia: int
    valor_mensal: float
    valor_total: float


class PlanoUpdate(PlanoBase):
    pass


class AssinarPlano(BaseModel):
    aluno_id: int
    plano_id: int
