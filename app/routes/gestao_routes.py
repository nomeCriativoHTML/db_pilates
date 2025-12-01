from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.aluno import AlunoUpdate
from app.schema.professor import ProfessorUpdate
from app.schema.estudio import EstudioUpdate
from app.database.connection import get_db
from app.models.aluno import Aluno
from app.models.professor import Professor
from app.models.estudio import Estudio
from app.models.relacionamentos.agenda import Agenda



router = APIRouter(
    prefix="/gestao",
    tags=["Gestão / Dashboard"]
)

# ================================
# Listar alunos
# ================================
@router.get("/dados/alunos")
def api_listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Aluno).all()
    return [
        {
            "id": a.id,
            "nome": a.nome,
            "cpf": a.cpf,
            "email": a.email,
            "status_pagamento": a.status_pagamento.value
        }
        for a in alunos
    ]


# ================================
# Listar professores
# ================================
@router.get("/dados/professores")
def api_listar_professores(db: Session = Depends(get_db)):
    profs = db.query(Professor).all()
    return [
        {
            "id": p.id,
            "nome": p.nome,
            "email": p.email,
            "cref": p.cref,
            "identificador": p.identificador,
            "tipo_identificador": p.tipo_identificador,
            "ativo": p.ativo,
            "estudio_id": p.estudio_id
        }
        for p in profs
    ]


# ================================
# Listar estúdios
# ================================
@router.get("/dados/estudios")
def api_listar_estudios(db: Session = Depends(get_db)):
    estudios = db.query(Estudio).all()
    return [
        {
            "id": e.id,
            "nome": e.nome,
            "endereco": e.endereco,
            "cep": e.cep,
            "telefone": e.telefone,
            "email": e.email,
            "capacidade_maxima": e.capacidade_maxima
        }
        for e in estudios
    ]


# ================================
# Listar agendas
# ================================
# ================================
# Listar TODAS as agendas
# ================================
@router.get("/dados/agendas")
def api_listar_agendas(db: Session = Depends(get_db)):
    agendas = db.query(Agenda).order_by(Agenda.data.asc(), Agenda.hora.asc()).all()

    return [
        {
            "id": a.id,
            "data": a.data.isoformat(),
            "hora": a.hora.strftime("%H:%M"),
            "tipo_aula": a.tipo_aula,
            "professor_id": a.professor_id,
            "estudio_id": a.estudio_id,
            "bloqueado": a.bloqueado,
            "motivo_bloqueio": a.motivo_bloqueio
        }
        for a in agendas
    ]

# ================================
# Pagamentos atrasados
# ================================
@router.get("/dados/pagamentos_atrasados")
def api_pagamentos_atrasados(db: Session = Depends(get_db)):
    atrasados = db.query(Aluno).filter(
        Aluno.status_pagamento.in_(["pendente", "atrasado"])
    ).all()

    return [
        {
            "id": a.id,
            "nome": a.nome,
            "cpf": a.cpf,
            "email": a.email,
            "status_pagamento": a.status_pagamento.value
        }
        for a in atrasados
    ]

# ================================
# EXCLUIR ALUNO
# ================================
@router.delete("/aluno/{id}")
def excluir_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()

    if not aluno:
        return {"erro": "Aluno não encontrado"}

    db.delete(aluno)
    db.commit()
    return {"mensagem": "Aluno excluído com sucesso"}


# ================================
# EXCLUIR PROFESSOR
# ================================
@router.delete("/professor/{id}")
def excluir_professor(id: int, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.id == id).first()

    if not professor:
        return {"erro": "Professor não encontrado"}

    db.delete(professor)
    db.commit()
    return {"mensagem": "Professor excluído com sucesso"}

# ================================
# EXCLUIR ESTÚDIO
# ================================
@router.delete("/estudio/{id}")
def excluir_estudio(id: int, db: Session = Depends(get_db)):
    estudio = db.query(Estudio).filter(Estudio.id == id).first()

    if not estudio:
        return {"erro": "Estúdio não encontrado"}

    db.delete(estudio)
    db.commit()
    return {"mensagem": "Estúdio excluído com sucesso"}


# ================================
# EDITAR ALUNO
# ================================
@router.put("/aluno/{id}")
def editar_aluno(id: int, dados: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    for campo, valor in dados.dict(exclude_unset=True).items():
        setattr(aluno, campo, valor)

    db.commit()
    db.refresh(aluno)

    return {"mensagem": "Aluno atualizado com sucesso"}


# ================================
# EDITAR PROFESSOR
# ================================

@router.put("/professor/{id}")
def editar_professor(
    id: int,
    dados: ProfessorUpdate,
    db: Session = Depends(get_db),
):
    professor = db.query(Professor).filter(Professor.id == id).first()

    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    update_data = dados.model_dump(exclude_unset=True)

    for campo, valor in update_data.items():
        if hasattr(professor, campo):
            setattr(professor, campo, valor)

    db.commit()
    db.refresh(professor)

    return {"mensagem": "Professor atualizado com sucesso"}



# ================================
# EDITAR ESTUDIO
# ================================

@router.put("/estudio/{id}")
def editar_estudio(id: int, dados: dict, db: Session = Depends(get_db)):
    estudio = db.query(Estudio).filter(Estudio.id == id).first()

    if not estudio:
        raise HTTPException(status_code=404, detail="Estúdio não encontrado")

    # Remover campos vazios ("")
    dados_filtrados = {k: v for k, v in dados.items() if v not in ["", None]}

    for campo, valor in dados_filtrados.items():
        setattr(estudio, campo, valor)

    db.commit()
    db.refresh(estudio)

    return {"mensagem": "Estúdio atualizado com sucesso"}



# ================================
# Listar agendas
# ================================


@router.get("/dados/agendas")
def api_listar_agendas(db: Session = Depends(get_db)):
    agendas = db.query(Agenda).all()
    return [
        {
            "id": a.id,
            "data": str(a.data),
            "hora": str(a.hora),
            "tipo_aula": a.tipo_aula,
            "status": a.status.value,
            "professor_id": a.professor_id,
            "substituto_id": a.substituto_id,
            "estudio_id": a.estudio_id,
            "bloqueado": a.bloqueado,
            "motivo_bloqueio": a.motivo_bloqueio
        }
        for a in agendas
    ]
