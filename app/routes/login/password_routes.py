from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.controllers.login.password_controller import PasswordResetController
from app.schema.login.password_reset import (
    PasswordResetRequest,
    PasswordResetVerify, 
    PasswordResetConfirm
)
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/password", tags=["Recuperação de Senha"])

# =======================
# PÁGINAS HTML
# =======================

@router.get("/reset", response_class=HTMLResponse)
async def pagina_recuperar_senha(request: Request, error: str = None, success: str = None):
    """
    Renderiza a página de recuperação de senha.
    """
    return templates.TemplateResponse(
        "recuperar_senha.html",
        {
            "request": request, 
            "error": error,
            "success": success
        }
    )

@router.get("/reset/confirmar", response_class=HTMLResponse)
async def pagina_confirmar_senha(
    request: Request, 
    token: str = None, 
    email: str = None,
    error: str = None
):
    """
    Renderiza a página para definir nova senha.
    """
    if not token or not email:
        return templates.TemplateResponse(
            "recuperar_senha.html",
            {
                "request": request,
                "error": "Token ou email inválido"
            }
        )
    
    return templates.TemplateResponse(
        "nova_senha.html",
        {
            "request": request,
            "token": token,
            "email": email,
            "error": error
        }
    )

# =======================
# ENDPOINTS API - FORMULÁRIO
# =======================

@router.post("/reset/request")
async def solicitar_recuperacao_senha(request: Request, db: Session = Depends(get_db)):
    """
    Recebe solicitação de recuperação de senha via formulário.
    """
    try:
        data = await request.form()
        email = data.get("email")
        user_type = data.get("user_type", "aluno")  # Default para aluno

        reset_request = PasswordResetRequest(email=email, user_type=user_type)
        resultado = PasswordResetController.request_password_reset(db, reset_request)

        return JSONResponse(
            content={
                "message": resultado["message"],
                "success": resultado["success"],
                "redirect": f"/password/reset/token?email={email}"
            }
        )

    except HTTPException as e:
        return JSONResponse(
            content={"error": e.detail},
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Erro inesperado: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/reset/verify")
async def verificar_token_form(request: Request, db: Session = Depends(get_db)):
    """
    Verifica token via formulário.
    """
    try:
        data = await request.form()
        token = data.get("token")
        email = data.get("email")

        verify_request = PasswordResetVerify(token=token, email=email)
        resultado = PasswordResetController.verify_token(db, verify_request)

        return JSONResponse(content=resultado)

    except HTTPException as e:
        return JSONResponse(
            content={"error": e.detail},
            status_code=e.status_code
        )

@router.post("/reset/confirm")
async def confirmar_nova_senha(request: Request, db: Session = Depends(get_db)):
    """
    Confirma nova senha via formulário.
    """
    try:
        data = await request.form()
        token = data.get("token")
        email = data.get("email")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        confirm_request = PasswordResetConfirm(
            token=token,
            email=email,
            new_password=new_password,
            confirm_password=confirm_password
        )

        resultado = PasswordResetController.reset_password(db, confirm_request)

        return JSONResponse(
            content={
                "message": resultado["message"],
                "success": resultado["success"],
                "redirect": "/login"  # Redirecionar para login após sucesso
            }
        )

    except HTTPException as e:
        return JSONResponse(
            content={"error": e.detail},
            status_code=e.status_code
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Erro inesperado: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# =======================
# ENDPOINTS API - JSON
# =======================

@router.post("/reset/request/api")
def solicitar_recuperacao_senha_api(
    reset_request: PasswordResetRequest, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para solicitação de recuperação de senha via API JSON.
    """
    return PasswordResetController.request_password_reset(db, reset_request)

@router.post("/reset/verify/api")
def verificar_token_api(
    verify_request: PasswordResetVerify, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para verificação de token via API JSON.
    """
    return PasswordResetController.verify_token(db, verify_request)

@router.post("/reset/confirm/api")
def confirmar_nova_senha_api(
    confirm_request: PasswordResetConfirm, 
    db: Session = Depends(get_db)
):
    """
    Endpoint para confirmação de nova senha via API JSON.
    """
    return PasswordResetController.reset_password(db, confirm_request)

# =======================
# INSERIR TOKEN PÁGINA
# =======================


@router.get("/reset/token", response_class=HTMLResponse)
async def pagina_inserir_token(request: Request, email: str = None, error: str = None):
    """
    Renderiza a página para inserir o token.
    """
    if not email:
        return templates.TemplateResponse(
            "recuperar_senha.html",
            {
                "request": request,
                "error": "Email é necessário"
            }
        )
    
    return templates.TemplateResponse(
        "inserir_token.html",
        {
            "request": request,
            "email": email,
            "error": error
        }
    )