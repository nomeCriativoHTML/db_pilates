from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.controllers.admin_controller import AdminController
from app.schema.admin import AdminCreate, AdminUpdate

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/admins",
    tags=["Admins / Recepção"]
)

# =====================================================
# PÁGINAS HTML
# =====================================================

@router.get("/cadastro", response_class=HTMLResponse)
async def pagina_cadastro_admin(request: Request, success: bool = False, error: str = None):
    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request, "success": success, "error": error}
    )

# =====================================================
# FORM POST VIA FRONT-END
# =====================================================

@router.post("/cadastro")
async def criar_admin_form(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()

        admin_data = AdminCreate(
            nome=data.get("nome"),
            email=data.get("email"),
            senha=data.get("senha"),
            tipo_admin=data.get("tipo_admin"),   
            status=data.get("status", "ativo")
        )

        AdminController.criar_admin(db, admin_data)

        return JSONResponse(
            {"message": "Administrador cadastrado com sucesso!"},
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# =====================================================
# API REST
# =====================================================

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_admin_api(admin: AdminCreate, db: Session = Depends(get_db)):
    return AdminController.criar_admin(db, admin)

@router.get("/")
def listar_admins(db: Session = Depends(get_db)):
    return AdminController.listar_admins(db)

@router.get("/{admin_id}")
def obter_admin(admin_id: int, db: Session = Depends(get_db)):
    return AdminController.obter_admin(db, admin_id)

@router.put("/{admin_id}")
def atualizar_admin(admin_id: int, admin_data: AdminUpdate, db: Session = Depends(get_db)):
    return AdminController.atualizar_admin(db, admin_id, admin_data)

@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_admin(admin_id: int, db: Session = Depends(get_db)):
    return AdminController.excluir_admin(db, admin_id)
