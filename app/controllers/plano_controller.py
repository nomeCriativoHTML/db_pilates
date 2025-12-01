from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.plano import Plano
from app.models.aluno import Aluno
from app.schema.plano_schema import AssinarPlano

class PlanoController:

    # ==========================
    # LISTAR TODOS OS PLANOS
    # ==========================
# controller.py
    @staticmethod
    def listar_planos(db: Session):
        planos = db.query(Plano).all()
        return [
            {
                "id": plano.id,
                "periodo": plano.periodo,
                "frequencia": plano.frequencia,
                "valor_mensal": float(plano.valor_mensal),
                "valor_total": float(plano.valor_total),
                "politica_cancelamento": plano.politica_cancelamento
            } 
            for plano in planos
        ]


    # ==========================
    # BUSCAR UM PLANO PELO ID
    # ==========================
    @staticmethod
    def buscar_plano(plano_id: int, db: Session):
        plano = db.query(Plano).filter(Plano.id == plano_id).first()
        if not plano:
            raise HTTPException(status_code=404, detail="Plano não encontrado")
        return plano

    # ==========================
    # ALUNO ASSINAR UM PLANO
    # ==========================
    @staticmethod
    def aluno_assinar_plano(aluno_id: int, plano_id: int, db: Session):
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

        plano = db.query(Plano).filter(Plano.id == plano_id).first()
        if not plano:
            raise HTTPException(status_code=404, detail="Plano não encontrado")

        aluno.plano_id = plano.id
        aluno.status_pagamento = "pendente"  
        db.commit()
        db.refresh(aluno)
        return {
            "detail": "Plano assinado com sucesso",
            "aluno": aluno.nome,
            "plano": plano.periodo,
            "valor_mensal": plano.valor_mensal,
            "valor_total": plano.valor_total
        }
