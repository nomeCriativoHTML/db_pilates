from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.estudio import Estudio
from app.schema.estudio import EstudioCreate, EstudioUpdate

class EstudioController:

    @staticmethod
    def criar_estudio(db: Session, estudio: EstudioCreate):
        # Verificar campos obrigatórios
        if not estudio.nome:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome do estúdio é obrigatório."
            )
        if not estudio.endereco:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Endereço do estúdio é obrigatório."
            )
        if not estudio.cep:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CEP do estúdio é obrigatório."
            )

        # Verificar se já existe estúdio com mesmo nome e CEP
        estudio_existente = db.query(Estudio).filter(
            (Estudio.nome == estudio.nome) & (Estudio.cep == estudio.cep)
        ).first()
        if estudio_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estúdio com mesmo nome e CEP já cadastrado."
            )

        # Criar novo estúdio
        novo_estudio = Estudio(
            nome=estudio.nome,
            endereco=estudio.endereco,
            cep=estudio.cep,
            telefone=estudio.telefone,
            email=estudio.email,
            capacidade_maxima=estudio.capacidade_maxima
        )

        db.add(novo_estudio)
        db.commit()
        db.refresh(novo_estudio)
        return novo_estudio

    @staticmethod
    def listar_estudios(db: Session):
        return db.query(Estudio).all()

    @staticmethod
    def obter_estudio(db: Session, estudio_id: int):
        estudio = db.query(Estudio).filter(Estudio.id == estudio_id).first()
        if not estudio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estúdio não encontrado."
            )
        return estudio

    @staticmethod
    def atualizar_estudio(db: Session, estudio_id: int, estudio_data: EstudioUpdate):
        estudio = db.query(Estudio).filter(Estudio.id == estudio_id).first()
        if not estudio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estúdio não encontrado."
            )

        update_data = estudio_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(estudio, key, value)

        db.commit()
        db.refresh(estudio)
        return estudio

    @staticmethod
    def excluir_estudio(db: Session, estudio_id: int):
        estudio = db.query(Estudio).filter(Estudio.id == estudio_id).first()
        if not estudio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estúdio não encontrado."
            )

        db.delete(estudio)
        db.commit()
        return {"mensagem": f"Estúdio '{estudio.nome}' excluído com sucesso."}
