from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.controllers.aluno_controller import AlunoController
from app.schema.aluno import AlunoCreate, AlunoUpdate

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)

# =====================================================
# PÁGINAS HTML (Renderizadas com Jinja2)
# =====================================================

@router.get("/cadastro", response_class=HTMLResponse)
async def pagina_cadastro(request: Request, success: bool = False, error: str = None):
    """
    Exibe a página de cadastro de alunos.
    Pode exibir mensagem de sucesso/erro após submissão do formulário.
    """
    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request, "success": success, "error": error}
    )

@router.post("/cadastro/aluno")
async def criar_aluno_form(request: Request, db: Session = Depends(get_db)):
    """
    Recebe os dados do formulário via JSON e cria um aluno no banco.
    Retorna uma resposta JSON para o front.
    """
    try:
        data = await request.json()

        aluno_data = AlunoCreate(
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            email=data.get("email"),
            senha=data.get("senha"),
            telefone=data.get("telefone"),
            data_nascimento=data.get("data_nascimento"),
            status_pagamento=data.get("status_pagamento", "pendente")
        )

        AlunoController.criar_aluno(db, aluno_data)

        return JSONResponse(
            content={"message": "Aluno cadastrado com sucesso!"},
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

#RENDERIZA A PAGINA DE ALUNOS APOS O LOGIN
@router.get("/aluno", response_class=HTMLResponse)
async def pagina_aluno(request: Request):
    """
    Página principal do aluno após login.
    """
    return templates.TemplateResponse("aluno.html", {"request": request})


@router.get("/agenda", response_class=HTMLResponse)
async def pagina_agenda(request: Request):
    """
    Página de agenda do aluno.
    """
    return templates.TemplateResponse("agenda.html", {"request": request})



#AQUI O ALUNO SE CADASTRA CASO NÃO TENHA CONTA
@router.get("/cadastrar", response_class=HTMLResponse)
async def pagina_cadastro_aluno(request: Request):
    return templates.TemplateResponse(
        "cadastro_aluno.html",
        {"request": request}
    )



@router.post("/cadastrar")
async def cadastrar_aluno_json(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()

        aluno_data = AlunoCreate(
            nome=data.get("nome"),
            cpf=data.get("cpf"),
            email=data.get("email"),
            senha=data.get("senha"),
            telefone=data.get("telefone"),
            data_nascimento=data.get("data_nascimento"),
            status_pagamento="pendente"
        )

        AlunoController.criar_aluno(db, aluno_data)

        return JSONResponse(
            {"message": "Cadastro realizado com sucesso!"},
            status_code=201
        )

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=400
        )


# =====================================================
# ENDPOINTS RESTFUL (API)
# =====================================================

@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def criar_aluno_api(aluno: AlunoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo aluno via API.
    """
    return AlunoController.criar_aluno(db, aluno)

@router.get("/", response_model=None)
def listar_alunos(db: Session = Depends(get_db)):
    """
    Lista todos os alunos.
    """
    return AlunoController.listar_alunos(db)

@router.get("/{aluno_id}", response_model=None)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Retorna um aluno específico pelo ID.
    """
    return AlunoController.obter_aluno(db, aluno_id)

@router.put("/{aluno_id}", response_model=None)
def atualizar_aluno(aluno_id: int, aluno_data: AlunoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um aluno existente.
    """
    return AlunoController.atualizar_aluno(db, aluno_id, aluno_data)

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """
    Exclui um aluno pelo ID.
    """
    return AlunoController.excluir_aluno(db, aluno_id)
