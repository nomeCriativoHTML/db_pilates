from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.controllers.estudio_controller import EstudioController
from app.schema.estudio import EstudioCreate, EstudioUpdate

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/estudios",
    tags=["Estudios"]
)

# =====================================================
# PÁGINAS HTML (Renderizadas com Jinja2)
# =====================================================

@router.get("/cadastro", response_class=HTMLResponse)
async def pagina_cadastro_estudio(request: Request, success: bool = False, error: str = None):
    """
    Exibe a página de cadastro de estúdios.
    Pode exibir mensagem de sucesso/erro após submissão do formulário.
    """
    return templates.TemplateResponse(
        "estudio.html",  # template HTML que você deve criar para cadastro de estúdios
        {"request": request, "success": success, "error": error}
    )

@router.post("/cadastro/estudio")
async def criar_estudio_form(request: Request, db: Session = Depends(get_db)):
    """
    Recebe os dados do formulário via JSON e cria um estúdio no banco.
    Retorna uma resposta JSON para o front.
    """
    try:
        data = await request.json()

        estudio_data = EstudioCreate(
            nome=data.get("nome"),
            endereco=data.get("endereco"),
            cep=data.get("cep"),
            telefone=data.get("telefone"),
            email=data.get("email"),
            capacidade_maxima=data.get("capacidade_maxima", 3)
        )

        EstudioController.criar_estudio(db, estudio_data)

        return JSONResponse(
            content={"message": "Estúdio cadastrado com sucesso!"},
            status_code=status.HTTP_201_CREATED
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

# =====================================================
# ENDPOINTS RESTFUL (API)
# =====================================================

@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def criar_estudio_api(estudio: EstudioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo estúdio via API.
    """
    return EstudioController.criar_estudio(db, estudio)

@router.get("/", response_model=None)
def listar_estudios(db: Session = Depends(get_db)):
    """
    Lista todos os estúdios.
    """
    return EstudioController.listar_estudios(db)

@router.get("/{estudio_id}", response_model=None)
def obter_estudio(estudio_id: int, db: Session = Depends(get_db)):
    """
    Retorna um estúdio específico pelo ID.
    """
    return EstudioController.obter_estudio(db, estudio_id)

@router.put("/{estudio_id}", response_model=None)
def atualizar_estudio(estudio_id: int, estudio_data: EstudioUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um estúdio existente.
    """
    return EstudioController.atualizar_estudio(db, estudio_id, estudio_data)

@router.delete("/{estudio_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_estudio(estudio_id: int, db: Session = Depends(get_db)):
    """
    Exclui um estúdio pelo ID.
    """
    return EstudioController.excluir_estudio(db, estudio_id)
