from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn
import time

# =========================================================
# Inicialização do app
# =========================================================
app = FastAPI(
    title="Sistema Pilates",
    description="API do Sistema de Gestão de Alunos e Aulas",
    version="1.0.0"
)

# =========================================================
# Configuração de templates e arquivos estáticos
# =========================================================
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Adiciona o "time" como variável global do Jinja2
templates.env.globals['time'] = int(time.time())

# =========================================================
# Middleware CORS
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Importação e inclusão de rotas
# =========================================================
from app.routes import aluno_routes 
app.include_router(aluno_routes.router)

from app.routes.professor_routes import router as professor_router
app.include_router(professor_router)

from app.routes.estudio_routes import router as estudio_router
app.include_router(estudio_router)

from app.routes.admin_routes import router as admin_router
app.include_router(admin_router)

from app.routes.login.aluno_login import router as aluno_login_router
app.include_router(aluno_login_router)  

from app.routes.login.professor_login import router as professor_login_router
app.include_router(professor_login_router) 

from app.routes.login.admin_login import router as admin_login_router
app.include_router(admin_login_router)

from app.routes.gestao_routes import router as gestao_router
app.include_router(gestao_router)

from app.routes.agenda_routes import router as agenda_router
app.include_router(agenda_router)

from app.routes import plano_routes
app.include_router(plano_routes.router)


# =========================================================
# NOVAS ROTAS DE RECUPERAÇÃO DE SENHA
# =========================================================
from app.routes.login.password_routes import router as password_router
app.include_router(password_router)

# =========================================================
# Rotas básicas
# =========================================================
@app.get("/", include_in_schema=False)
async def root():
    """Redireciona para a página de login"""
    return RedirectResponse(url="/login/")

# =========================================================
# Inicialização do servidor
# =========================================================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
