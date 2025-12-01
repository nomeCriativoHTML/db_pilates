from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from datetime import datetime
from app.controllers.login.aluno_login import AlunoLoginController
from app.schema.login.aluno_login import AlunoLogin
from fastapi.templating import Jinja2Templates
from app.models.plano import Plano
from app.utils.security import get_current_aluno
from app.models.professor import AlunoNaAula
from app.models.enums import Presenca

from app.models.relacionamentos.agenda import Agenda
from app.models.relacionamentos.agendamentos import Agendamento
from app.models.enums import StatusAula

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/login", tags=["Login Aluno"])

# =======================
# Página HTML de login
# =======================
@router.get("/", response_class=HTMLResponse)
async def pagina_login(request: Request, error: str = None):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error}
    )

# =======================
# Login via formulário HTML
# =======================
@router.post("/aluno")
async def login_aluno_form(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.form()
        email = data.get("email")
        senha = data.get("password")

        resultado = AlunoLoginController.login_aluno(
            db, AlunoLogin(email=email, senha=senha)
        )

        token = resultado["token"]

        response = JSONResponse({
            "message": resultado["message"],
            "redirect": "/login/aluno"
        })

        response.set_cookie(
            key="aluno_access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24,
        )

        return response

    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Erro inesperado: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# =======================
# Login via API JSON
# =======================
@router.post("/aluno/api")
def login_aluno_api(dados: AlunoLogin, db: Session = Depends(get_db)):
    return AlunoLoginController.login_aluno(db, dados)


# =======================
# PÁGINA PRINCIPAL DO ALUNO
# =======================
@router.get("/aluno", response_class=HTMLResponse)
async def pagina_aluno(
    request: Request,
    aluno = Depends(get_current_aluno),
    db: Session = Depends(get_db)
):
    data_formatada = datetime.now().strftime("%d/%m/%Y")

    # Busca o plano do aluno
    plano = db.query(Plano).filter(Plano.id == aluno.plano_id).first()
    possui_plano = plano is not None

    # =======================
    # BUSCA AS AULAS DISPONÍVEIS
    # =======================
    aulas = (
        db.query(Agenda)
        .filter(Agenda.status == StatusAula.disponivel)
        .order_by(Agenda.data.asc(), Agenda.hora.asc())
        .all()
    )

    return templates.TemplateResponse(
        "aluno.html",
        {
            "request": request,
            "aluno": aluno,
            "plano": plano,
            "possui_plano": possui_plano,
            "data_atual": data_formatada,
            "aulas_disponiveis": aulas  # <<--- ENVIADO PARA O HTML
        }
    )


# =======================
# API: DETALHES DA AULA
# =======================
@router.get("/aluno/aula/{aula_id}")
def detalhes_aula(aula_id: int, db: Session = Depends(get_db)):
    aula = db.query(Agenda).filter(Agenda.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")

    return {
        "id": aula.id,
        "data": aula.data.strftime("%d/%m/%Y"),
        "hora": aula.hora.strftime("%H:%M"),
        "professor": aula.professor.nome if aula.professor else None,
        "estudio": aula.estudio.nome if aula.estudio else None,
        "endereco": getattr(aula.estudio, "endereco", None),
        "tipo_aula": aula.tipo_aula,
        "max_alunos": aula.max_alunos,
        "vagas_restantes": aula.max_alunos - len(aula.agendamentos),
        "status": aula.status.value,
    }


# =======================
# API: INSCREVER O ALUNO NA AULA
# =======================
@router.post("/aluno/aula/confirmar/{aula_id}")
def confirmar_aula(
    aula_id: int,
    aluno = Depends(get_current_aluno),
    db: Session = Depends(get_db)
):
    """
    Inscreve o aluno em uma aula usando Agendamento.
    Unifica o fluxo com o que o professor vê.
    """

    # 1. Aula existe?
    aula = db.query(Agenda).filter(Agenda.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")

    # 2. Já inscrito?
    ja_tem = db.query(Agendamento).filter(
        Agendamento.aluno_id == aluno.id,
        Agendamento.aula_id == aula_id
    ).first()
    if ja_tem:
        return {"message": "Você já está inscrito nesta aula."}

    # 3. Checar vagas
    vagas = db.query(Agendamento).filter(Agendamento.aula_id == aula_id).count()
    if vagas >= aula.max_alunos:
        return JSONResponse({"message": "A aula está cheia."}, status_code=400)

    # 4. Criar o agendamento
    novo = Agendamento(aluno_id=aluno.id, aula_id=aula_id)
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"message": "Inscrição realizada com sucesso!"}



