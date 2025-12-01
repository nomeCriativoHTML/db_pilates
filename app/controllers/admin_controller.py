from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.admin import Admin
from app.schema.admin import AdminCreate, AdminUpdate
from app.utils.security import hash_senha


class AdminController:

    @staticmethod
    def criar_admin(db: Session, admin: AdminCreate):
        # Verificar se email já existe
        admin_existente = db.query(Admin).filter(Admin.email == admin.email).first()
        if admin_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um administrador com esse e-mail."
            )

        # Criar novo admin com senha criptografada
        novo_admin = Admin(
            nome=admin.nome,
            email=admin.email,
            senha=hash_senha(admin.senha),
            tipo_admin=admin.tipo_admin,
            ativo=True
        )

        db.add(novo_admin)
        db.commit()
        db.refresh(novo_admin)

        return novo_admin

    @staticmethod
    def listar_admins(db: Session):
        return db.query(Admin).all()

    @staticmethod
    def obter_admin(db: Session, admin_id: int):
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado."
            )
        return admin

    @staticmethod
    def atualizar_admin(db: Session, admin_id: int, admin_data: AdminUpdate):
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado."
            )

        update_data = admin_data.model_dump(exclude_unset=True)

        # Se veio senha nova, criptografar
        if "senha" in update_data and update_data["senha"]:
            update_data["senha"] = hash_senha(update_data["senha"])

        for key, value in update_data.items():
            setattr(admin, key, value)

        db.commit()
        db.refresh(admin)

        return admin

    @staticmethod
    def excluir_admin(db: Session, admin_id: int):
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Administrador não encontrado."
            )

        db.delete(admin)
        db.commit()

        return {"mensagem": f"Administrador {admin.nome} removido com sucesso."}
