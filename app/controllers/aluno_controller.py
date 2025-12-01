from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.utils.security import hash_senha
from app.models.aluno import Aluno
from app.schema.aluno import AlunoCreate, AlunoUpdate

class AlunoController:

    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoCreate):
        # Verificar se já existe aluno com mesmo CPF ou email
        aluno_existente = db.query(Aluno).filter(
            (Aluno.email == aluno.email) | (Aluno.cpf == aluno.cpf)
        ).first()
        if aluno_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aluno com CPF ou email já cadastrado."
            )

        # Criar novo aluno com hash SHA-256
        novo_aluno = Aluno(
            nome=aluno.nome,
            cpf=aluno.cpf,
            telefone=aluno.telefone,
            email=aluno.email,
            senha=hash_senha(aluno.senha),
            data_nascimento=aluno.data_nascimento,
            status_pagamento=aluno.status_pagamento
        )

        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return novo_aluno

    @staticmethod
    def listar_alunos(db: Session):
        return db.query(Aluno).all()

    @staticmethod
    def obter_aluno(db: Session, aluno_id: int):
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )
        return aluno

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, aluno_data: AlunoUpdate):
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )

        update_data = aluno_data.model_dump(exclude_unset=True)
        if "senha" in update_data:
            update_data["senha"] = hash_senha(update_data["senha"])

        for key, value in update_data.items():
            setattr(aluno, key, value)

        db.commit()
        db.refresh(aluno)
        return aluno

    @staticmethod
    def excluir_aluno(db: Session, aluno_id: int):
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )

        db.delete(aluno)
        db.commit()
        return {"mensagem": f"Aluno {aluno.nome} excluído com sucesso."}

    @staticmethod
    def criar_aluno_publico(db: Session, dados: AlunoCreate):
        
        # Regra de validação – evita duplicados
        aluno_existente = db.query(Aluno).filter(Aluno.email == dados.email).first()
        if aluno_existente:
            raise HTTPException(
                status_code=400,
                detail="Este email já está cadastrado."
            )

        novo_aluno = Aluno(
            nome=dados.nome,
            email=dados.email,
            senha=hash_senha(dados.senha),  # mesma função de hash usada no admin
            telefone=dados.telefone,
            ativo=True
        )

        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)

        return novo_aluno
