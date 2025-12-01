from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.utils.security import hash_senha
from app.models.professor import Professor
from app.schema.professor import ProfessorCreate, ProfessorUpdate

class ProfessorController:

    @staticmethod
    def criar_professor(db: Session, professor: ProfessorCreate):
        # Verificar campos obrigatórios
        if not professor.cref:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CREF é obrigatório."
            )
        
        if not professor.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email é obrigatório."
            )

        # Verificar se já existe professor com mesmo email ou CREf
        professor_existente = db.query(Professor).filter(
            (Professor.email == professor.email) | (Professor.cref == professor.cref)
        ).first()
        if professor_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Professor com email ou CREf já cadastrado."
            )

        # Se estudio_id foi fornecido, verificar se existe
        if professor.estudio_id:
            from app.models.estudio import Estudio
            estudio = db.query(Estudio).filter(Estudio.id == professor.estudio_id).first()
            if not estudio:
                # Em vez de dar erro, podemos setar como null
                professor.estudio_id = None

        # Criar novo professor
        novo_professor = Professor(
            nome=professor.nome,
            cref=professor.cref,
            email=professor.email,
            senha=hash_senha(professor.senha),
            identificador=professor.identificador,
            tipo_identificador=professor.tipo_identificador,
            ativo=professor.ativo,
            estudio_id=professor.estudio_id
        )

        db.add(novo_professor)
        db.commit()
        db.refresh(novo_professor)
        return novo_professor

    @staticmethod
    def listar_professores(db: Session):
        return db.query(Professor).all()

    @staticmethod
    def obter_professor(db: Session, professor_id: int):
        professor = db.query(Professor).filter(Professor.id == professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado."
            )
        return professor

    @staticmethod
    def atualizar_professor(db: Session, professor_id: int, professor_data: ProfessorUpdate):
        professor = db.query(Professor).filter(Professor.id == professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado."
            )

        update_data = professor_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(professor, key, value)

        db.commit()
        db.refresh(professor)
        return professor

    @staticmethod
    def excluir_professor(db: Session, professor_id: int):
        professor = db.query(Professor).filter(Professor.id == professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado."
            )

        db.delete(professor)
        db.commit()
        return {"mensagem": f"Professor {professor.nome} excluído com sucesso."}