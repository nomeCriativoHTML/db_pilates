import enum

class StatusPagamento(enum.Enum):
    pendente = "pendente"
    pago = "pago"
    atrasado = "atrasado"

class StatusAgendamento(enum.Enum):
    disponivel = "disponivel"
    reservado = "reservado"
    cancelado = "cancelado"

class TipoIdentificador(enum.Enum):
    cpf = "cpf"
    rg = "rg"
    outro = "outro"

class StatusAula(enum.Enum):
    disponivel = "disponivel"
    em_andamento = "em_andamento"
    finalizada = "finalizada"

class Presenca(enum.Enum):
    presente = "presente"
    ausente = "ausente"
    indefinido = "indefinido"

class Status(enum.Enum):
    ativo = "ativo"
    inativo = "inativo"
    pendente = "pendente"

class TipoAdmin(enum.Enum):
    pleno = "admin_pleno"
    recepcionista = "recepcionista"
