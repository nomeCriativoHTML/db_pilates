from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.controllers.plano_controller import PlanoController
from app.schema.plano_schema import PlanoCreate, PlanoUpdate, AssinarPlano

router = APIRouter(prefix="/planos", tags=["Planos"])

# ==========================
# LISTAR PLANOS
# ==========================
@router.get("/")
def listar_planos(db: Session = Depends(get_db)):
    return PlanoController.listar_planos(db)

# ==========================
# BUSCAR UM PLANO PELO ID
# ==========================
@router.get("/{plano_id}")
def buscar_plano(plano_id: int, db: Session = Depends(get_db)):
    return PlanoController.buscar_plano(plano_id, db)

# ==========================
# CRIAR NOVO PLANO
# ==========================
@router.post("/")
def criar_plano(data: PlanoCreate, db: Session = Depends(get_db)):
    return PlanoController.criar_plano(data, db)

# ==========================
# ATUALIZAR PLANO
# ==========================
@router.put("/{plano_id}")
def atualizar_plano(plano_id: int, data: PlanoUpdate, db: Session = Depends(get_db)):
    return PlanoController.atualizar_plano(plano_id, data, db)

# ==========================
# DELETAR PLANO
# ==========================
@router.delete("/{plano_id}")
def deletar_plano(plano_id: int, db: Session = Depends(get_db)):
    return PlanoController.deletar_plano(plano_id, db)

# ==========================
# ASSINAR PLANO PELO ALUNO
# ==========================
@router.post("/assinar")
def assinar_plano(data: AssinarPlano, db: Session = Depends(get_db)):
    return PlanoController.aluno_assinar_plano(
        aluno_id=data.aluno_id,
        plano_id=data.plano_id,
        db=db
    )

