from fastapi import APIRouter, Depends, Request, HTTPException, status
from datetime import datetime
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.models.relacionamentos.agenda import Agenda
from app.database.connection import get_db
from app.controllers.agenda_controller import AgendaController
from app.schema.agenda import AgendaCreate, AgendaUpdate, BloqueioAgenda
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/agendas",
    tags=["Agenda / Horários"]
)

# =====================================================
# PÁGINAS HTML
# =====================================================

@router.get("/cadastro", response_class=HTMLResponse)
async def pagina_cadastro_agenda(request: Request):
    return templates.TemplateResponse(
        "agenda_cadastro.html",
        {"request": request}
    )

# =====================================================
# FORM POST VIA FRONT END
# =====================================================

@router.post("/cadastro")
async def criar_agenda_form(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        agenda_data = AgendaCreate(**data)
        AgendaController.criar_agenda(db, agenda_data)

        return JSONResponse(
            {"message": "Agenda cadastrada com sucesso!"},
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# =====================================================
# API REST PADRÃO
# =====================================================

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_agenda_api(dados: AgendaCreate, db: Session = Depends(get_db)):
    return AgendaController.criar_agenda(db, dados)


@router.get("/")
def listar_agendas(db: Session = Depends(get_db)):
    return AgendaController.listar_agendas(db)


@router.put("/{agenda_id}")
def atualizar_agenda(agenda_id: int, dados: AgendaUpdate, db: Session = Depends(get_db)):
    return AgendaController.atualizar_agenda(db, agenda_id, dados)


@router.delete("/{agenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_agenda(agenda_id: int, db: Session = Depends(get_db)):
    return AgendaController.excluir_agenda(db, agenda_id)

# =====================================================
# AÇÕES ESPECIAIS — COLOCAR ANTES DE /{agenda_id}
# =====================================================

@router.patch("/{agenda_id}/bloquear")
async def bloquear_agenda(
    agenda_id: int,
    dados: BloqueioAgenda,
    db: Session = Depends(get_db)
):
    return AgendaController.bloquear_agenda(db, agenda_id, dados.motivo)


@router.patch("/{agenda_id}/desbloquear")
def desbloquear_agenda(agenda_id: int, db: Session = Depends(get_db)):
    return AgendaController.desbloquear_agenda(db, agenda_id)

# =====================================================
# FILTROS IMPORTANTES
# =====================================================

@router.get("/dia/{data}")
def listar_agendas_por_dia(data: str, db: Session = Depends(get_db)):
    try:
        data_convertida = datetime.strptime(data, "%Y-%m-%d").date()
    except:
        raise HTTPException(
            status_code=400,
            detail="Formato de data inválido. Use YYYY-MM-DD."
        )

    return db.query(Agenda).filter(
        Agenda.data == data_convertida
    ).order_by(Agenda.hora).all()


@router.get("/professor/{professor_id}")
def listar_por_professor(professor_id: int, db: Session = Depends(get_db)):
    return db.query(Agenda).filter(
        Agenda.professor_id == professor_id
    ).order_by(Agenda.data, Agenda.hora).all()


@router.get("/estudio/{estudio_id}")
def listar_por_estudio(estudio_id: int, db: Session = Depends(get_db)):
    return db.query(Agenda).filter(
        Agenda.estudio_id == estudio_id
    ).order_by(Agenda.data, Agenda.hora).all()

# =====================================================
# ÚLTIMA ROTA — PARA NÃO QUEBRAR NADA
# =====================================================

@router.get("/{agenda_id}")
def obter_agenda(agenda_id: int, db: Session = Depends(get_db)):
    return AgendaController.obter_agenda(db, agenda_id)

# =====================================================
# PÁGINA HTML DE LISTAGEM COMPLETA
# =====================================================

@router.get("/agendas", response_class=HTMLResponse)
def listar_agendas_html(request: Request, db: Session = Depends(get_db)):
    agendas = AgendaController.listar_agendas(db)
    return templates.TemplateResponse(
        "agendas/listar_agendas.html",
        {"request": request, "agendas": agendas}
    )
