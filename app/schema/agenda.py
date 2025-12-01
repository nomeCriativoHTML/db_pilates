from pydantic import BaseModel, ConfigDict, validator
from datetime import date, time
from typing import Optional
from app.models.enums import StatusAula

class AgendaBase(BaseModel):
    estudio_id: int
    professor_id: int
    substituto_id: Optional[int] = None
    data: date
    hora: time
    tipo_aula: Optional[str] = None
    max_alunos: int = 3
    status: Optional[StatusAula] = StatusAula.disponivel
    bloqueado: Optional[bool] = False
    motivo_bloqueio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @validator("motivo_bloqueio", always=True)
    def motivo_obrigatorio_quando_bloqueado(cls, v, values):
        # se veio bloqueado True, motivo é obrigatório
        if values.get("bloqueado") is True and (v is None or str(v).strip() == ""):
            raise ValueError("motivo_bloqueio é obrigatório quando bloqueado=True")
        return v

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(BaseModel):
    
    estudio_id: Optional[int] = None
    professor_id: Optional[int] = None
    substituto_id: Optional[int] = None
    data: Optional[date] = None
    hora: Optional[time] = None
    tipo_aula: Optional[str] = None
    max_alunos: Optional[int] = None
    status: Optional[StatusAula] = None
    bloqueado: Optional[bool] = None
    motivo_bloqueio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @validator("motivo_bloqueio", always=True)
    def motivo_obrigatorio_quando_bloqueado_update(cls, v, values):
        # validação só se bloqueado for setado explicitamente como True
        if "bloqueado" in values and values.get("bloqueado") is True:
            if v is None or str(v).strip() == "":
                raise ValueError("motivo_bloqueio é obrigatório quando bloquear a agenda")
        return v

class AgendaOut(AgendaBase):
    id: int
    professor_nome: Optional[str] = None
    estudio_nome: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)



class BloqueioAgenda(BaseModel):
    motivo: str





