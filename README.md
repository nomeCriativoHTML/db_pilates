# Sistema Pilates - Gestão de Aulas e Alunos

Sistema web de gestão para estúdios de pilates, desenvolvido com **FastAPI**, **SQLAlchemy** e **Jinja2**. Gerencia alunos, professores, estúdios, agendas e agendamentos de aulas.

## Visão Geral

Uma plataforma completa para gerenciar:
- **Alunos**: cadastro, autenticação e visualização de evolução
- **Professores**: gestão de turmas e agendas
- **Estúdios**: múltiplas unidades de negócio
- **Agenda**: configuração de disponibilidade
- **Agendamentos**: inscrição em aulas
- **Administração**: gestão de todo o sistema

---

## Estrutura do Projeto

```
Pilates/
├── main.py                          # Aplicação FastAPI principal
├── alembic.ini                      # Configuração Alembic (migrações)
├── requirements.txt                 # Dependências Python
├── .env                             # Variáveis de ambiente
│
├── alembic/
│   ├── env.py                       # Ambiente de migrações
│   ├── script.py.mako               # Template de migração
│   ├── versions/                    # Migrações do banco
│   │   └── d1206559d37f_initial.py
│
└── app/
    ├── database/
    │   └── connection.py            # Configuração SQLAlchemy, get_db()
    │
    ├── models/                      # Modelos SQLAlchemy
    │   ├── admin.py
    │   ├── aluno.py
    │   ├── professor.py
    │   ├── estudio.py
    │   ├── enums.py
    │   └── relacionamentos/
    │       ├── agenda.py
    │       └── agendamentos.py
    │
    ├── schema/                      # Schemas Pydantic (validação)
    │   ├── admin.py
    │   ├── aluno.py
    │   ├── professor.py
    │   ├── estudio.py
    │   ├── agenda.py
    │   └── login/
    │       ├── admin_login.py
    │       ├── aluno_login.py
    │       └── professor_login.py
    │
    ├── controllers/                 # Lógica de negócio
    │   ├── admin_controller.py
    │   ├── aluno_controller.py
    │   ├── professor_controller.py
    │   ├── estudio_controller.py
    │   ├── agenda_controller.py
    │   ├── gestao_controller.py
    │   └── login/
    │       ├── admin_login.py
    │       ├── aluno_login.py
    │       └── professor_login.py
    │
    ├── routes/                      # Endpoints FastAPI
    │   ├── admin_routes.py
    │   ├── aluno_routes.py
    │   ├── professor_routes.py
    │   ├── estudio_routes.py
    │   ├── agenda_routes.py
    │   ├── gestao_routes.py
    │   └── login/
    │       ├── admin_login.py
    │       ├── aluno_login.py
    │       └── professor_login.py
    │
    ├── templates/                   # Templates Jinja2 (HTML)
    │   ├── login.html
    │   ├── cadastro.html
    │   ├── aluno.html
    │   ├── professor.html
    │   ├── estudio.html
    │   ├── admin.html
    │   ├── agenda.html
    │   └── evolucao.html
    │
    ├── static/                      # Arquivos estáticos
    │   ├── CSS/
    │   │   ├── logins.css
    │   │   ├── cadastro.css
    │   │   ├── alunos.css
    │   │   ├── professor.css
    │   │   ├── estudio.css
    │   │   ├── admin.css
    │   │   ├── agenda.css
    │   │   └── evolucao.css
    │   ├── JS/
    │   │   ├── logins.js
    │   │   ├── cadastros.js
    │   │   ├── aluno.js
    │   │   ├── professor.js
    │   │   ├── admin.js
    │   │   └── agenda.js
    │   └── img/
    │
    └── utils/
        └── security.py              # Utilitários de segurança
```

---

## Arquitetura e Fluxo

### Camadas de Processamento
1. **Routes** (`app/routes/`) → Recebe requisições HTTP, injeta dependências
2. **Controllers** (`app/controllers/`) → Implementa regras de negócio
3. **Models** (`app/models/`) → Representação de dados (SQLAlchemy ORM)
4. **Schema** (`app/schema/`) → Validação e serialização (Pydantic)
5. **Database** (`app/database/`) → Conexão e sessão com BD
6. **Templates/Static** → Interface web renderizada (Jinja2 + HTML/CSS/JS)

### Fluxo de Requisição
```
Cliente HTTP
    ↓
FastAPI Router (routes/)
    ↓
Controller (lógica de negócio)
    ↓
Models (SQLAlchemy - BD)
    ↓
Schema (validação)
    ↓
Response (JSON ou HTML)
```

---

## Como Executar

### Pré-requisitos
- Python 3.8+
- MySQL (ou banco configurável via .env)
- pip

### Instalação Local

1. **Ativar ambiente virtual:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variáveis de ambiente:**
   
   Crie/edite `.env`:
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost:3306/pilates_db
   SECRET_KEY=sua_chave_secreta_aqui
   ```

4. **Executar migrações:**
   ```bash
   alembic upgrade head
   ```

5. **Iniciar servidor:**
   ```bash
   uvicorn main:app --reload
   ```
   
   Acesse: `http://127.0.0.1:8000`

---

## Principais Endpoints

### Autenticação (Login)
- `GET /login/` — Página de login
- `POST /login/aluno` — Login de aluno
- `POST /login/professor` — Login de professor
- `POST /login/admin` — Login de admin

### Alunos
- `GET /alunos/cadastro` — Página de cadastro
- `GET /alunos/{id}` — Perfil do aluno
- `POST /api/alunos/` — Criar aluno
- `GET /evolucao/{aluno_id}` — Evolução/histórico

### Professores
- `GET /professores/` — Listagem
- `POST /api/professores/` — Criar professor

### Estúdios
- `GET /studios/` — Listagem
- `POST /api/studios/` — Criar estúdio

### Agenda
- `GET /agenda/` — Visualizar agenda
- `POST /api/agendamentos/` — Agendar aula

### Gestão/Admin
- `GET /admin/` — Dashboard admin
- `GET /gestao/` — Gestão geral

---

## Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| **fastapi** | latest | Framework web |
| **uvicorn** | 0.27.1 | Servidor ASGI |
| **sqlalchemy** | 2.0.29 | ORM |
| **alembic** | 1.13.1 | Migrações BD |
| **pymysql** | 1.1.0 | Driver MySQL |
| **jinja2** | 3.1.2 | Templates |
| **pydantic** | 2.6.1 | Validação |
| **python-dotenv** | 1.0.0 | Variáveis de ambiente |
| **PyJWT** | 2.8.0 | Autenticação JWT |

Lista completa em `requirements.txt`.

---

## Segurança

- **Autenticação**: JWT/Sessão (implementado em `app/utils/security.py`)
- **Validação**: Todos os inputs validados via Pydantic schemas
- **CORS**: Habilitado para múltiplas origens
- **Hash**: Senhas encriptadas com `cryptography`

---

## Notas Importantes

- **Banco de Dados**: Conexão centralizada em `app/database/connection.py`
- **Migrações**: Use `alembic` para versionamento do schema
- **Templates**: Renderizadas com Jinja2, acesso a `time` global
- **Static Files**: Montados em `/static/` automaticamente
- **Organização**: Sempre manter separação: routes → controllers → models

---

## Como Contribuir

1. Siga a estrutura: **routes → controllers → models → schema**
2. Crie schemas Pydantic para validação
3. Implemente lógica em controllers
4. Mantenha models limpos (apenas ORM)
5. Antes de commitar: verifique migrações com `alembic upgrade head`

---

## Licença

Este projeto é parte do Sistema Pilates.

---

**Última atualização:** Novembro 2025
