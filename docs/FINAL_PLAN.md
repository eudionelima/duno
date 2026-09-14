# PLANO FINAL — DUNO

> **Arquivo mestre de implementação — DUNO — Designed Unsecure Network Operations**
> Estado encontrado: **somente especificação (docs + README + LICENSE). Nenhum código implementado.**
> Regra: outro Desenvolvedor deve conseguir executar todas as etapas seguintes lendo **somente este arquivo + o código futuro do projeto**.

---

## ÍNDICE

1. Visão geral do projeto
2. Stack tecnológica atual
3. Arquitetura atual
4. Estrutura de diretórios
5. Fluxo da aplicação
6. Backend
7. Banco de dados SQLite
8. Frontend
9. Docker
10. Documentação existente
11. Estado atual do projeto
12. Análise de segurança
13. Problemas e prioridades
14. Plano de implementação futuro
15. Alterações por arquivo
16. Banco de dados — alterações futuras
17. Docker — alterações futuras
18. Frontend — alterações futuras
19. Backend — alterações futuras
20. Testes
21. Critérios de conclusão do projeto
22. Ordem recomendada de execução
23. Regras para a Próximo DESENVOLVEDOR

---

## 1. Visão geral do projeto

### 1.1. O que é o DUNO

DUNO — *Designed Unsecure Network Operations* — é especificado como **plataforma web deliberadamente vulnerável, monolítica e dockerizada, para treinamento prático de segurança de aplicações web e APIs**.

Inspiração funcional: DVWA / bWAPP / OWASP Juice Shop, mas com escopo próprio:

- 19 módulos de vulnerabilidades web clássicas + 1 módulo especial de API Security (total 20 entradas no dashboard).
- Cada módulo implementa 4 níveis didáticos: `low` → `medium` → `high` → `impossible` (vulnerável → mitigação básica → mitigação incompleta → seguro).
- Recursos globais: seletor de nível por módulo, `View Source` (visualização do código do nível), `Reset Database`, dashboard central, autenticação de laboratório.

### 1.2. Finalidade

Laboratório controlado para:

- estudar vulnerabilidades na prática;
- comparar código vulnerável vs. mitigado vs. seguro;
- treinar exploração manual e uso de ferramentas (Burp, curl, scripts);
- treinar defesa (revisão de código, validação, prepared statements, CSP, CSRF tokens, rate limit, JWT, etc.).

### 1.3. Estado atual encontrado (fato verificado em disco)

Verificação executada:

```powershell
Get-ChildItem -LiteralPath "C:\Users\dione\Downloads\duno" -Recurse -Force
```

Resultado — **12 arquivos/diretórios no total, nenhum código-fonte executável**:

```text
duno/
├── LICENSE                      # MIT, Copyright (c) 2026 Dione Lima
├── README.md                     # visão geral, módulos, rotas, Docker, docs
└── docs/
    ├── ARCHITECTURE.md
    ├── BUILD_GUIDE.md
    ├── DATABASE.md
    ├── DEPLOYMENT.md
    ├── DEVELOPMENT.md
    ├── MODULES.md
    ├── ROADMAP.md
    ├── SECURITY.md
    └── SECURITY_LEVELS.md
```

**Não existe** (verificado — ausência total):

- `Dockerfile`, `docker-compose.yml`, `entrypoint.sh`, `requirements.txt`
- `run.py`, `config.py`, `seed.py`, `app.py` / `wsgi.py`
- `core/`, `modules/`, `templates/`, `static/`, `data/`
- Qualquer `.py`, `.html`, `.css`, `.js`, `.db`, `.sqlite`, `.env`, `.dockerignore`
- Testes, CI, scripts, `.git` (informado pelo ambiente: `Is directory a git repo: no`)

Ou seja: **o projeto está em estágio 100% especificação, 0% implementação**. Toda a arquitetura, rotas, tabelas, fluxos e padrões descritos nos `docs/` são **intenção documentada, não código verificado**. Não há divergência código-vs-doc porque não há código; há apenas **lacuna total entre especificação e implementação**.

### 1.4. Implicação para o próximo Desenvolvedor

O próximo DESENVOLVEDOR **não fará manutenção incremental**. Ela fará **construção greenfield guiada pela especificação**. Este plano, portanto, detalha:

- o que a especificação exige (extraído dos 9 docs);
- o que está ausente e precisa ser criado arquivo a arquivo;
- como cada parte deve funcionar e se comunicar;
- em que ordem construir para não quebrar dependências;
- como validar cada entrega em Docker.

---

## 2. Stack tecnológica atual

### 2.1. Stack especificada (não ainda instalada/verificada)

Nenhuma tecnologia foi encontrada instalada no repositório (sem `requirements.txt`, sem `Dockerfile`). A tabela abaixo é **o que os docs exigem**, e onde cada tecnologia deverá ser usada:

| Tecnologia | Versão exigida | Onde será usada | Como | Status real |
|---|---|---|---|---|
| Python | 3.11 | Todo backend Flask, `seed.py`, scripts | Imagem base `python:3.11-slim` no Dockerfile | Não implementado |
| Flask | 3.x | `run.py`/`app factory`, `core/*`, `modules/*/routes.py` | Blueprints por módulo, Jinja2, sessões server-side via cookie assinado | Não implementado |
| SQLite | 3.x (embutido no Python) | `data/duno.db` → `/app/data/duno.db` | Acesso via `sqlite3` stdlib, helper central `core/database.py`, sem ORM obrigatório | Arquivo inexistente, schema só documentado |
| HTML | HTML5 | `templates/*.html`, `templates/modules/*.html` | Jinja2 extends `base.html`, formulários POST, sem framework | Não implementado |
| CSS | CSS3 puro | `static/css/duno.css` | Layout dark lab, dashboard cards, formulários, modal, responsivo | Não implementado |
| JavaScript Vanilla | ES6 sem framework | `static/js/duno.js`, `static/js/view_source.js` | fetch para `/level`, `/reset`, `/source`, XSS DOM lab, sem jQuery/React/Vue | Não implementado |
| Prism.js (opcional) | via CDN | Modal View Source | Syntax highlight `language-python`; prever fallback sem CDN (offline) | Não implementado, decisão pendente |
| Docker | 24+ | `Dockerfile` | Build single-container `duno-app` | Arquivo inexistente |
| Docker Compose | v2 (`docker compose` / `docker-compose`) | `docker-compose.yml` | Serviço único, porta `2300:2300`, volume `./data:/app/data` | Arquivo inexistente |
| SQLite persistência | volume bind | `docker-compose.yml` | `./data:/app/data` | Não implementado |
| Gunicorn/Werkzeug | — | Produção lab | Docs citam apenas `Flask`; decidir: dev `flask run` vs `gunicorn`. Recomendação neste plano: `gunicorn` opcional, padrão Werkzeug dev server aceitável para lab, mas documentar | Não decidido |

### 2.2. O que NÃO usar (proibição explícita dos docs)

- **Não** introduzir VM (VirtualBox, Vagrant, VMware) como requisito, etapa ou alternativa.
- **Não** migrar para Django, FastAPI, Node, PHP, MySQL/Postgres, ORM pesado (SQLAlchemy permitido mas não exigido; preferência por `sqlite3` puro para didática do SQLi).
- **Não** introduzir framework frontend (React, Vue, Angular, jQuery, Bootstrap JS). CSS puro; Prism.js via CDN é a única exceção tolerada.
- **Não** renomear o projeto; usar sempre `DUNO — Designed Unsecure Network Operations`. Não usar nomes anteriores (nenhum citado, mas proibido ressuscitar).

### 2.3. Dependências Python previstas (a criar em `requirements.txt`)

Versões a pinar na implementação (compatíveis com Python 3.11 + Flask 3.x em 2026):

```text
Flask==3.1.0
Werkzeug==3.1.3
Jinja2==3.1.4
itsdangerous==2.2.0
click==8.1.7
PyJWT==2.10.1          # módulo API Security / crypto
cryptography==44.0.0   # módulo crypto (didático)
gunicorn==23.0.0       # opcional, execução no container
```

> O próximo DESENVOLVEDOR criará `requirements.txt` e validará via `docker-compose up --build`.

---

## 3. Arquitetura atual

### 3.1. Arquitetura especificada (alvo) vs. arquitetura real

**Alvo documentado** (`ARCHITECTURE.md` + `README.md`):

```text
Docker Host
└── Container: duno-app (único)
    ├── entrypoint.sh
    │   ├── banner ASCII
    │   ├── if [ ! -f /app/data/duno.db ]; then python seed.py; fi
    │   └── exec python run.py  (ou gunicorn)
    ├── Flask Application (monolito, Blueprints)
    │   ├── Core (cross-cutting)
    │   ├── 19 Web Blueprints + 1 API Blueprint
    │   ├── Templates (Jinja2) + Static (CSS/JS)
    │   └── SQLite via volume
    └── SQLite: /app/data/duno.db
```

**Arquitetura real hoje**: inexistente. Não há container, imagem, processo Flask ou arquivo DB. Há apenas texto descrevendo o alvo acima.

### 3.2. Backend (especificado)

- Padrão: **monolito Flask + Blueprints**, sem microserviços.
- App factory sugerida (não imposta, mas recomendada neste plano): `create_app()` em `app.py` ou `core/__init__.py`, registrada por `run.py`.
- `core/` com 6 arquivos transversais: `database.py`, `security_levels.py`, `reset.py`, `source_loader.py`, `auth.py`, `decorators.py`.
- `modules/<mod>/{__init__.py, routes.py, logic.py, source/{low,medium,high,impossible}.py}`.
- Blueprints registados centralmente; cada um expõe `GET+POST /<rota>` no mínimo.

### 3.3. Banco de dados (especificado)

- SQLite arquivo único, caminho canônico `/app/data/duno.db` (container) ↔ `data/duno.db` (host).
- 7 tabelas documentadas (detalhes na Seção 7).
- Criação via `seed.py`; `entrypoint.sh` só semeia se o arquivo não existir; `POST /reset` restaura dados de laboratório.

### 3.4. Frontend (especificado)

```text
templates/
├── base.html                  # layout, nav, seletor global?, footer
├── index.html                 # dashboard com 20 cards
├── login.html                 # login lab
├── _level_switch.html         # partial: form POST /level/<module>
├── _view_source_modal.html    # partial: modal + <pre><code>
└── modules/
    ├── brute_force.html
    ├── ... (um por módulo, ~20 arquivos)
    └── api_security.html

static/
├── css/duno.css
├── js/duno.js                 # level switch, reset, helpers
├── js/view_source.js          # fetch GET /source/<mod>/<lvl> → modal + Prism
└── uploads/                   # destino File Upload (deve existir + .gitkeep)
```

Comunicação: formulários HTML `POST` clássicos + `fetch` JS para `/level`, `/reset`, `/source` (JSON ou HTML fragment). Sem SPA, sem build step.

### 3.5. Docker (especificado)

- Um serviço, uma imagem, uma porta (`2300:2300`), um volume (`./data:/app/data`).
- Inicialização: `docker-compose up --build` → build → `entrypoint.sh` → seed se necessário → Flask em `0.0.0.0:2300`.
- Sem networks custom, sem healthcheck, sem múltiplos containers, sem Postgres/Redis.

### 3.6. Comunicação entre componentes (fluxo canônico a implementar)

```text
Browser ──HTTP :2300──▶ Flask (duno-app)
  │  GET /                      → index.html (dashboard)
  │  GET /login ↔ POST /login   → auth.py + users
  │  GET /<module>              → routes.py → logic.get_<mod>(level) → template
  │  POST /<module>             → routes.py → logic.dispatch(level, input) → template+resultado
  │  POST /level/<module>       → security_levels.py → UPDATE security_levels
  │  GET /source/<mod>/<level>  → source_loader.py (importlib/inspect) → código .py
  │  POST /reset                → reset.py → re-seed tabelas de lab
  │  /api/*                     → api_security blueprint (JSON + JWT)
  └─▶ SQLite /app/data/duno.db via core/database.py (get_db, query, execute)
```

---

## 4. Estrutura de diretórios

### 4.1. Estrutura encontrada (real)

```text
duno/
├── LICENSE
├── README.md
└── docs/ (9 .md)
```

Nada mais. Sem diretórios ocultos, sem código.

### 4.2. Estrutura alvo (a ser criadO pelO próximo DESENVOLVEDOR — normativa)

Baseada em `README.md § Estrutura do repositório` + `ARCHITECTURE.md §4` + `DEVELOPMENT.md` + `BUILD_GUIDE.md`, consolidada e completada aqui (a Próximo DESENVOLVEDOR deve seguir exatamente esta árvore; desvios precisam justificativa):

```text
duno/
├── Dockerfile                    # NOVO — python:3.11-slim, Flask :2300
├── docker-compose.yml            # NOVO — serviço duno-app, 2300:2300, ./data:/app/data
├── .dockerignore                 # NOVO — excluir data/*.db, __pycache__, .git, docs grandes?
├── entrypoint.sh                 # NOVO — banner + seed condicional + exec Flask (chmod +x)
├── requirements.txt              # NOVO — Flask 3.x + PyJWT + cryptography + gunicorn
├── run.py                        # NOVO — entrypoint Python (create_app + app.run 0.0.0.0:2300)
├── config.py                     # NOVO — SECRET_KEY via env, DATABASE_PATH, UPLOAD_FOLDER, etc.
├── seed.py                       # NOVO — DDL + inserts iniciais (idempotente)
├── app.py  (ou core/__init__.py) # NOVO — create_app(), registro de Blueprints, rotas globais
├── data/
│   ├── .gitkeep                  # NOVO — manter dir versionado sem commitar .db
│   └── duno.db                   # GERADO em runtime (NÃO commitar; .gitignore)
├── core/
│   ├── __init__.py               # NOVO
│   ├── database.py               # NOVO — get_db(), init_db(), query helpers
│   ├── security_levels.py        # NOVO — get_level(), set_level(), validação low|medium|high|impossible
│   ├── reset.py                  # NOVO — reset_lab_data()
│   ├── source_loader.py          # NOVO — importlib + inspect.getsource()
│   ├── auth.py                   # NOVO — login/logout, hash, sessão
│   └── decorators.py             # NOVO — login_required, level_context?
├── modules/
│   ├── __init__.py               # NOVO — import/registro helper (opcional)
│   ├── brute_force/ ... (×20, ver §4.3)
│   └── api_security/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── _level_switch.html
│   ├── _view_source_modal.html
│   └── modules/*.html (×20)
├── static/
│   ├── css/duno.css
│   ├── js/duno.js
│   ├── js/view_source.js
│   └── uploads/.gitkeep
├── docs/ (existente — atualizar quando arquitetura mudar)
├── .gitignore                    # NOVO — data/*.db, __pycache__, *.pyc, .env
├── .env.example                  # NOVO — SECRET_KEY placeholder, FLASK_ENV
└── FINAL_PLAN.md (este arquivo — manter, não apagar)
```

### 4.3. Padrão por módulo (20× repetição, obrigatório)

Para cada `mod` em `[brute_force, command_injection, csrf, file_inclusion, file_upload, captcha, sqli, sqli_blind, weak_session, xss_dom, xss_reflected, xss_stored, csp_bypass, js_attacks, auth_bypass, open_redirect, crypto, api_versioning, mass_assignment, api_security]`:

```text
modules/<mod>/
├── __init__.py        # cria Blueprint(name=<mod>, url_prefix? ou rota explícita)
├── routes.py          # GET+POST /<rota>, integra level + template
├── logic.py           # def low/medium/high/impossible + dispatcher
└── source/
    ├── __init__.py
    ├── low.py         # implementação didática vulnerável (espelho do logic low)
    ├── medium.py
    ├── high.py
    └── impossible.py  # implementação segura
```

Responsabilidades (conforme `DEVELOPMENT.md`):

| Arquivo | Responsabilidade | O que NÃO fazer |
|---|---|---|
| `__init__.py` | Criar/exportar `bp = Blueprint(...)` | Não colocar lógica de negócio aqui |
| `routes.py` | HTTP: ler `request.form/args/json`, obter level via `core.security_levels`, chamar `logic`, renderizar template | Não concatenar SQL, não `os.system` direto; delegar a `logic.py` |
| `logic.py` | Seleção por nível + execução; cada `def low(...)` documenta a falha didática | Não importar Flask `request`; receber parâmetros puros (testável) |
| `source/*.py` | Cópia fiel exibível via View Source; deve corresponder ao comportamento do nível | Não divergir de `logic.py` (risco: View Source mente) |

> Decisão arquitetural a preservar: `source/*.py` são a **fonte de verdade visual**; `logic.py` deve importar ou espelhar esses arquivos, nunca implementar lógica diferente da exibida. Estratégia recomendada: `logic.py` importa `from .source import low, medium...` ou delega explicitamente, para garantir fidelidade View Source.

### 4.4. Diretórios/arquivos relevantes explicados

- `core/database.py`: único ponto de acesso SQLite. Deve expor `get_db()`, `close_db()`, `init_db()`, helpers `query_db()`/`execute_db()`. Todas as queries de módulos passam por aqui (exceto SQLi low, que intencionalmente concatena — mas ainda via conexão central).
- `core/security_levels.py`: leitura/escrita da tabela `security_levels` por `(user_id, module)`. Valida `level in (...)`; default `low` se ausente.
- `core/auth.py`: login lab (`admin/password` seed), hash `werkzeug.security`, sessão Flask, `logout`, helper `current_user()`.
- `core/decorators.py`: `@login_required`, opcional `@admin_required` para `auth_bypass` lab.
- `core/source_loader.py`: `get_source(module, level)` com whitelist de módulos/níveis, `importlib.import_module(f"modules.{module}.source.{level}")` + `inspect.getsource()`. Nunca `open()` com path cru do usuário (evita LFI no próprio View Source).
- `core/reset.py`: apaga/reinsere dados voláteis (`guestbook`, `captcha_challenges`, `secrets` demo, etc.) sem apagar `users`/`security_levels`? Ou full re-seed? Decisão documentada na Seção 16 — a Próximo DESENVOLVEDOR deve implementar e documentar o comportamento escolhido.
- `seed.py`: DDL das 7 tabelas + inserts (admin, secrets demo, tokens demo, captcha demo). Idempotente (`IF NOT EXISTS`, `INSERT OR IGNORE`).
- `config.py`: `SECRET_KEY=os.getenv(...)`, `DATABASE=/app/data/duno.db`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`, `PREFERRED_URL_SCHEME`. Sem segredos hardcoded além do fallback lab.
- `templates/base.html`: nav (Dashboard, Login/Logout, Reset button, nível global?), blocos `{% block content %}`, inclusão de `duno.css`, `duno.js`, `view_source.js`, modal partial.
- `static/uploads/`: destino de `file_upload`; deve ser servido com cuidado (sem execução) e limpável via reset.

---

## 5. Fluxo da aplicação

### 5.1. Fluxo global (usuário → backend → banco → resposta)

```text
1. Operador: docker-compose up --build
2. Browser: http://localhost:2300
3. Flask: GET / → auth? → index.html (20 cards do MODULES.md)
4. Usuário clica card → GET /<modulo> (ex. /sqli)
   → routes.py: level = security_levels.get_level(user_id, "sqli") default low
   → render modules/sqli.html com _level_switch (nível atual) + form do lab
5. Usuário submete lab → POST /<modulo>
   → routes.py extrai input → logic.dispatch(level, input)
   → low: query concatenada / medium: blacklist / high: prepared+falha sessão / impossible: prepared+validação
   → resultado renderizado no mesmo template (tabela, mensagem, shell output simulado)
6. Usuário troca nível → POST /level/<module> {level=high}
   → security_levels.set_level() → UPDATE SQLite → redirect back + toast (duno.js)
7. Usuário clica View Source → JS fetch GET /source/<mod>/<level>
   → source_loader.get_source() → código Python → modal com Prism highlight
8. Usuário clica Reset → POST /reset
   → reset.reset_lab_data() → re-seed → redirect + confirmação
9. API labs → fetch/ curl /api/* com JSON + headers (Authorization: Bearer JWT, X-API-Version)
```

### 5.2. Fluxos por recurso global

**Autenticação** (a especificar em detalhe — docs só citam `admin/password`):

```text
GET /login → login.html (username, password)
POST /login → auth.authenticate(username, password)
  → sucesso: session["user_id"]=id, redirect /
  → falha: re-render com erro genérico (low: mensagem verbosa? medium+: genérica)
GET /logout → session.clear() → redirect /login
Decorador @login_required protege /<modulos>? Decisão: docs não explicitam.
Recomendação: dashboard e labs exigem login (como DVWA), exceto talvez /login.
Brute Force lab usa endpoint próprio /brute_force que permite tentativas sem lockout em low.
```

**Security Level**:

```text
POST /level/<module> (form ou fetch, campo level)
 → validar module ∈ whitelist 20 + level ∈ {low,medium,high,impossible}
 → INSERT ... ON CONFLICT(user_id, module) DO UPDATE (SQLite UPSERT)
 → 302 redirect para /<module> ou JSON {ok, level} se Accept: application/json
Proteção: exigir login + método POST (CSRF lab em low permite GET? Não — o switcher global deve ser POST com token em impossible; em low pode ser CSRFável de propósito? Decidir e documentar.)
```

**View Source**:

```text
Click [View Source] → view_source.js: fetch(`/source/${mod}/${level}`)
 → Flask GET /source/<module>/<level>
 → source_loader: whitelist + importlib + inspect.getsource
 → resposta JSON {module, level, code} ou texto puro
 → modal _view_source_modal.html injeta <code class="language-python"> + Prism.highlight
Erro: 404 se módulo/nível inválido; nunca stacktrace em produção lab.
```

**Reset**:

```text
POST /reset (botão no base.html, confirmação JS)
 → reset.py: DELETE FROM guestbook; DELETE FROM captcha_challenges; re-INSERT seeds; ...
 → preservar users + security_levels? (recomendado: preservar; documentar)
 → redirect / + flash "Database reset"
```

### 5.3. Fluxo Docker (inicialização)

```text
docker-compose up --build
  → docker build -t duno-app . (python:3.11-slim, pip install -r requirements.txt, COPY ., chmod +x entrypoint.sh)
  → volume ./data:/app/data montado (cria ./data se ausente)
  → entrypoint.sh:
      echo banner DUNO
      if [ ! -f /app/data/duno.db ]; then python seed.py; fi
      exec python run.py  (listen 0.0.0.0:2300)
  → logs exibem URL, módulos, níveis, tecnologias (exigência DEPLOYMENT.md § Verificação)
```

---

## 6. Backend

### 6.1. Aplicação Flask (a criar — nada existe hoje)

**Arquivo principal**: `run.py` + `app.py` (ou `core/__init__.py` como factory). Padrão exigido:

```python
# run.py (especificação — não criar agora)
from app import create_app
app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2300, debug=False)
```

`create_app()` deve:

1. `Flask(__name__, template_folder="templates", static_folder="static")`
2. `app.config.from_object("config")` + `app.secret_key`
3. `teardown_appcontext(close_db)`
4. Registrar `core` rotas globais (`/`, `/login`, `/logout`, `/level/<module>`, `/source/<module>/<level>`, `/reset`)
5. Registrar os 20 Blueprints via loop + `modules/__init__.py` ou lista explícita em `app.py`
6. Configurar `MAX_CONTENT_LENGTH` (uploads), `UPLOAD_FOLDER`, headers CSP base (que o lab `csp_bypass` manipula por rota)
7. Logging básico para `docker-compose logs`

### 6.2. Rotas (contrato normativo — todas a implementar)

| Método | Rota | Handler previsto | Função | Auth? |
|---|---|---|---|---|
| GET | `/` | `app.py:index` | Dashboard 20 cards | login_required (recomendado) |
| GET/POST | `/login` | `core/auth.py` | Login lab | pública |
| GET | `/logout` | `core/auth.py` | Limpa sessão | login |
| POST | `/level/<module>` | `core/security_levels.py` | Persiste nível | login |
| GET | `/source/<module>/<level>` | `core/source_loader.py` | Retorna código | login |
| POST | `/reset` | `core/reset.py` | Restaura lab | login (+ CSRF em impossible) |
| GET/POST | `/brute_force` | `modules/brute_force/routes.py` | Lab 1 | login |
| GET/POST | `/command_injection` | `modules/command_injection/routes.py` | Lab 2 | login |
| GET/POST | `/csrf` | `modules/csrf/routes.py` | Lab 3 | login |
| GET/POST | `/file_inclusion` | `modules/file_inclusion/routes.py` | Lab 4 | login |
| GET/POST | `/file_upload` | `modules/file_upload/routes.py` | Lab 5 | login |
| GET/POST | `/captcha` | `modules/captcha/routes.py` | Lab 6 | login |
| GET/POST | `/sqli` | `modules/sqli/routes.py` | Lab 7 | login |
| GET/POST | `/sqli_blind` | `modules/sqli_blind/routes.py` | Lab 8 | login |
| GET/POST | `/weak_session` | `modules/weak_session/routes.py` | Lab 9 | login |
| GET | `/xss_dom` | `modules/xss_dom/routes.py` | Lab 10 (JS lê `location.hash`/`?q`) | login |
| GET/POST | `/xss_reflected` | `modules/xss_reflected/routes.py` | Lab 11 | login |
| GET/POST | `/xss_stored` | `modules/xss_stored/routes.py` | Lab 12 (guestbook) | login |
| GET/POST | `/csp_bypass` | `modules/csp_bypass/routes.py` | Lab 13 | login |
| GET/POST | `/js_attacks` | `modules/js_attacks/routes.py` | Lab 14 | login |
| GET/POST | `/auth_bypass` | `modules/auth_bypass/routes.py` | Lab 15 | login |
| GET/POST | `/open_redirect` | `modules/open_redirect/routes.py` | Lab 16 | login |
| GET/POST | `/crypto` | `modules/crypto/routes.py` | Lab 17 | login |
| GET/POST | `/api_versioning` | `modules/api_versioning/routes.py` | Lab 18 | login |
| GET/POST | `/mass_assignment` | `modules/mass_assignment/routes.py` | Lab 19 | login |
| ANY | `/api/*` | `modules/api_security/routes.py` | Lab 20 (JSON, JWT, IDOR, rate) | token/JWT |

Detalhes de cada lab (comportamento didático esperado por nível — inferido de DVWA + `SECURITY_LEVELS.md`; a Próximo DESENVOLVEDOR deve implementar e documentar no template de cada módulo):

- **Brute Force**: low sem lockout/rate; medium com `sleep(2)`/tentativa + mensagem genérica; high com CAPTCHA/token + lockout após N; impossible com rate limit + audit_log + bloqueio + CSRF token.
- **Command Injection**: low `os.popen("ping "+ip)` direto; medium blacklist `;|&&` bypassável com `| `; high regex mais forte mas bypass com encoding; impossible allowlist IP + `subprocess.run([...], shell=False)` + validação `ipaddress`.
- **CSRF**: lab altera senha/email via GET em low, sem token; medium com `Referer` check bypassável; high com token previsível; impossible com token criptográfico por sessão + SameSite.
- **File Inclusion**: low `open("pages/"+page)` / `render_template(page)`; medium blacklist `../` bypass com `....//`; high allowlist parcial; impossible allowlist estrita + `safe_join`.
- **File Upload**: low qualquer extensão em `static/uploads/`; medium check MIME client-side; high blacklist `.php` bypass com `.phtml`; impossible allowlist `.jpg/.png` + verificação magic bytes + rename aleatório + fora de webroot executável.
- **CAPTCHA**: low reutilizável/sem validação server; medium validado mas sem `used=1`; high validado mas bypass via parâmetro; impossible token único + expiração + `used` flag.
- **SQLi**: low concatenação `SELECT * FROM users WHERE username='...' AND password='...'`; medium `mysqli_real_escape`-like bypass; high prepared mas com falha sessão (exemplo citado); impossible prepared + validação + menor privilégio.
- **SQLi Blind**: low boolean `EXISTS(...)` + resposta sim/não; medium time-based `sleep`; high filtragem parcial; impossible prepared (sem diferença observável).
- **Weak Session**: low `session_id = user_id` sequencial/cookie manipulável; medium hash MD5 previsível; high timestamp + salt fraco; impossible Flask session assinada + random `secrets.token_urlsafe`.
- **XSS DOM/Reflected/Stored**: low sem escape (`|safe`); medium `replace("<script>")` bypass com case/event handlers; high allowlist parcial; impossible `escape()` + CSP + HttpOnly. Stored usa `guestbook`.
- **CSP Bypass**: low sem header; medium `script-src 'self'` bypass com upload/inline; high nonce previsível; impossible nonce aleatório + `object-src 'none'` + `base-uri`.
- **JS Attacks**: low preço/role no hidden field ou localStorage confiado; impossible validação server-side via `secrets`/DB.
- **Auth Bypass**: low `?admin=true` ou cookie `role=user` editável; impossible verificação server `session role==admin` + decorador.
- **Open Redirect**: low `redirect(request.args["next"])`; impossible allowlist domínios relativos.
- **Crypto**: low ROT13/Base64/MD5 sem salt como "proteção"; impossible bcrypt/ Werkzeug hash + `cryptography.fernet` com chave de env.
- **API Versioning**: low `/api/v1/users` expõe campos sensíveis, `/v2` filtra; medium com header `X-API-Version` confiado; impossible versão default segura + depreciação.
- **Mass Assignment**: low `User(**request.json)` permite `role=admin`; impossible allowlist `["name","email"]`.
- **API Security (`/api/*`)**: JWT (none algorithm em low, weak secret em medium, expiração ignorada em high, verificação completa em impossible), IDOR (`/api/users/<id>` sem check), rate limit (ausente → audit em impossible), versionamento.

### 6.3. Controllers/Views (`routes.py`)

Padrão obrigatório por módulo:

```python
# padrão normativo para modules/<mod>/routes.py
from flask import Blueprint, render_template, request
from core.security_levels import get_level
from . import logic

bp = Blueprint("<mod>", __name__)

@bp.route("/<rota>", methods=["GET", "POST"])
def index():
    level = get_level("<mod>")  # lê session user_id + SQLite, default low
    result = None
    if request.method == "POST":
        result = logic.dispatch(level, request.form / request.files / request.json)
    return render_template("modules/<mod>.html", level=level, result=result)
```

### 6.4. Services (`logic.py`)

- Funções puras `def low(payload)`, `medium`, `high`, `impossible` + `def dispatch(level, payload)`.
- Sem acesso a `request`, `session`, `g`. Recebem dict/str e retornam dict/str. Isso permite teste unitário sem Flask.
- Devem importar espelhar `source/*.py` para fidelidade View Source.

### 6.5. Models

Sem ORM. "Models" = DDL em `seed.py` + helpers em `core/database.py`. Tabelas: `users`, `security_levels`, `guestbook`, `secrets`, `api_tokens`, `captcha_challenges`, `audit_log` (Seção 7).

### 6.6. Funções importantes (a criar)

| Função | Arquivo | Assinatura sugerida |
|---|---|---|
| `create_app` | `app.py` | `def create_app(test_config=None) -> Flask` |
| `get_db` / `close_db` / `init_db` | `core/database.py` | `get_db() -> sqlite3.Connection` |
| `get_level` / `set_level` | `core/security_levels.py` | `get_level(module: str) -> str` |
| `get_source` | `core/source_loader.py` | `get_source(module, level) -> str` |
| `reset_lab_data` | `core/reset.py` | `def reset_lab_data(preserve_users=True)` |
| `authenticate` / `logout` | `core/auth.py` | `def authenticate(u,p) -> user\|None` |
| `login_required` | `core/decorators.py` | decorador Flask |
| `dispatch` (×20) | `modules/*/logic.py` | `def dispatch(level, data)` |

### 6.7. APIs

- `GET /source/<module>/<level>` → JSON `{module, level, code}` (ou texto). Usado pelo modal.
- `POST /level/<module>` → form `level=` ou JSON; retorna redirect ou JSON.
- `POST /reset` → redirect ou JSON.
- `/api/*` → JSON REST: `GET /api/users/<id>`, `POST /api/login` (JWT), `GET /api/secrets?version=v1`, etc. A definir no módulo `api_security` com Swagger-like doc estática (ROADMAP cita Swagger UI — decidir: página `/api/docs` estática, sem dependência extra).

### 6.8. Validações

- Global: whitelist `module ∈ 20 nomes`, `level ∈ 4 valores`. Rejeitar com 404/400, nunca 500 com stacktrace.
- Por nível: low **não valida de propósito** (documentar como intencional); impossible valida com allowlist, tipos, tamanhos, `escape`, prepared statements, tokens.
- Uploads: `MAX_CONTENT_LENGTH=2MB`, allowlist extensões em impossible, rename com `secrets.token_hex`.

### 6.9. Tratamento de erros

- Handlers `404`, `400`, `500` com templates amigáveis (sem stacktrace em `debug=False`).
- Labs SQLi Blind / Command Injection devem capturar exceções e retornar mensagens didáticas, não tracebacks.
- `source_loader` retorna 404 para módulo/nível inválido (não `FileNotFound` cru).

### 6.10. Dependências entre módulos

- Todos dependem de `core.database` + `core.security_levels`.
- `xss_stored` ↔ `guestbook`; `captcha` ↔ `captcha_challenges`; `crypto`/`js_attacks` ↔ `secrets`; `api_security` ↔ `api_tokens` + `users`; `auth_bypass`/`brute_force` ↔ `users` + `audit_log`.
- `reset.py` depende do schema de todos (ordem de DELETE respeitando FK).
- Frontend `view_source.js` depende do contrato `GET /source`.

---

## 7. Banco de dados SQLite

### 7.1. Estado atual

- **Arquivo inexistente**. Nenhum `.db`, nenhum `seed.py`, nenhum DDL executado.
- Especificação completa em `docs/DATABASE.md` (7 tabelas). DDL abaixo é transcrição fiel da doc — a Próximo DESENVOLVEDOR deve usar como base, com melhorias da §7.5.

### 7.2. Tabelas, campos, tipos, chaves (conforme doc)

**`users`** — contas do laboratório:

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',              -- 'user' | 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Seed previsto: admin/password (hash Werkzeug), + users demo user/test
```

**`security_levels`** — nível por (usuário, módulo):

```sql
CREATE TABLE IF NOT EXISTS security_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    module TEXT NOT NULL,
    level TEXT NOT NULL CHECK(level IN ('low','medium','high','impossible')),
    UNIQUE(user_id, module),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**`guestbook`** — XSS Stored:

```sql
CREATE TABLE IF NOT EXISTS guestbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**`secrets`** — Cryptography + JS Attacks:

```sql
CREATE TABLE IF NOT EXISTS secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT,
    value TEXT
);
-- Seed: ('flag_demo','DUNO{...}'), ('price','100'), etc.
```

**`api_tokens`** — API Security:

```sql
CREATE TABLE IF NOT EXISTS api_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token TEXT,
    version TEXT
);
```

**`captcha_challenges`** — CAPTCHA:

```sql
CREATE TABLE IF NOT EXISTS captcha_challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge TEXT,
    answer TEXT,
    used INTEGER DEFAULT 0
);
```

**`audit_log`** — auditoria (Brute Force impossible, etc.):

```sql
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    ip TEXT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.3. Relacionamentos e índices

- Relacionamentos documentados: `security_levels.user_id → users.id`. Implícitos: `api_tokens.user_id → users.id`, `audit_log.user_id → users.id`. Sem FK declarada para os dois últimos na doc — **lacuna a corrigir** (adicionar FK + `ON DELETE CASCADE`).
- Índices: **nenhum documentado além de PK/UNIQUE**. Lacuna: consultas frequentes `security_levels(user_id, module)`, `users(username)`, `api_tokens(token)`, `audit_log(ts)` precisam de índices (Seção 16).
- Tipos: todos `TEXT/INTEGER/TIMESTAMP`. Sem `NOT NULL` consistente (`guestbook.name/message` nullable de propósito para lab? documentar).

### 7.4. Inicialização e acesso

- Inicialização especificada: `python seed.py` cria `data/duno.db` se ausente; `entrypoint.sh` automatiza. `seed.py` deve ser idempotente (`CREATE TABLE IF NOT EXISTS`, `INSERT OR IGNORE` / `SELECT COUNT` guard).
- Acesso: `core/database.py` com `sqlite3.connect(app.config["DATABASE"])`, `row_factory=sqlite3.Row`, `PRAGMA foreign_keys=ON`, `PRAGMA journal_mode=WAL` (melhoria para concorrência lab), `g`-scoped connection + `teardown`.
- Caminho: `config.DATABASE = os.getenv("DATABASE_PATH", "/app/data/duno.db")` com fallback local `data/duno.db` para dev fora do Docker (opcional, documentar).

### 7.5. Problemas no modelo atual + solução futura (sem implementar agora)

| # | Problema | Impacto | Solução futura (Próximo DESENVOLVEDOR) |
|---|---|---|---|
| DB-1 | Sem `seed.py`, sem DDL executável | Nada funciona | Criar `seed.py` com DDL acima + seeds + guards idempotentes |
| DB-2 | FK ausente em `api_tokens.user_id`, `audit_log.user_id` | Órfãos, reset inconsistente | Adicionar `FOREIGN KEY ... REFERENCES users(id) ON DELETE CASCADE` |
| DB-3 | Sem índices em `users(username)`, `api_tokens(token)`, `security_levels(user_id,module)` (além do UNIQUE), `audit_log(ts)` | Lentidão Brute Force/API | `CREATE INDEX IF NOT EXISTS ...` (Seção 16) |
| DB-4 | Sem `CHECK(role IN ('user','admin'))` | `role` arbitrário via Mass Assignment contamina além do lab | Manter sem CHECK de propósito? Decidir: lab Mass Assignment precisa permitir `admin`; CHECK restringiria o lab. **Manter sem CHECK e documentar como intencional** |
| DB-5 | `guestbook`/`secrets` sem `user_id` | Sem rastreabilidade, reset apaga tudo | Aceitável para lab; documentar que reset é global, não por usuário |
| DB-6 | Sem estratégia de migração | Alterar schema quebra `duno.db` existente no volume | `seed.py` com `PRAGMA user_version` + função `migrate()` incremental; reset recria; documentar `rm data/duno.db` como último recurso |
| DB-7 | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` sem timezone | Logs com hora local do container | Aceitável; documentar UTC; usar `DATETIME DEFAULT (strftime(...))` se necessário |
| DB-8 | Sem senha seed documentada além de `admin/password` | Próximo DESENVOLVEDOR pode semear senhas fracas diferentes | Fixar seeds: `admin/password` (admin), `user/password` (user), `test/test` opcional; hash com `generate_password_hash` |

---

## 8. Frontend

### 8.1. Estado atual

**Zero arquivos**. Nenhum `.html`, `.css`, `.js`. Especificação em `ARCHITECTURE.md §9-10`, `DEVELOPMENT.md § Frontend`, `BUILD_GUIDE.md`.

### 8.2. HTML / Templates (a criar)

| Arquivo | Finalidade | Conteúdo obrigatório |
|---|---|---|
| `templates/base.html` | Layout global | `<!doctype>`, `<head>` com `duno.css`, nav (logo DUNO, Dashboard, Login/Logout, usuário atual, botão Reset), `{% block content %}`, `{% include "_view_source_modal.html" %}`, `<script>` `duno.js` + `view_source.js` + Prism CDN opcional |
| `templates/index.html` | Dashboard | `{% extends "base.html" %}`, grid de 20 cards (nome, descrição curta, rota, nível atual badge, links [Acessar] [View Source]), aviso "deliberadamente vulnerável" |
| `templates/login.html` | Login | Form `POST /login`, campos `username/password`, erro genérico, hint lab `admin/password` |
| `templates/_level_switch.html` | Partial reutilizável | Form `POST /level/<module>` com `<select low|medium|high|impossible>` + botão; usado via `{% include %}` em cada `modules/*.html` |
| `templates/_view_source_modal.html` | Modal | `<div id="vs-modal">` + `<pre><code id="vs-code">` + botões por nível |
| `templates/modules/*.html` (20) | Labs | Extends base, inclui `_level_switch`, form específico do lab, área `result`, botão View Source com `data-module` |

Convenções: Jinja2 `{{ result|safe }}` **somente** nos labs XSS low (intencional, comentado `<!-- INTENTIONALLY UNSAFE: XSS lab low -->`); em todos os outros, escape padrão `{{ ... }}`.

### 8.3. CSS (a criar: `static/css/duno.css`)

- CSS puro, sem framework. Tema dark lab (fundo `#0f1420`, acento `#e63946`/`#00d4ff` — decidir paleta e fixar).
- Componentes: nav, cards grid responsivo, forms, inputs, buttons, badges de nível (`low=vermelho`, `medium=laranja`, `high=amarelo`, `impossible=verde`), modal, `<pre>` código, tabelas de resultado, alertas.
- Responsivo: `@media (max-width: 768px)` single column; sem dependência Bootstrap.

### 8.4. JavaScript (a criar, Vanilla, sem build)

**`static/js/duno.js`**: seletor de nível via `fetch` (progressive enhancement: form funciona sem JS), reset com `confirm()`, helpers `toast()`, `csrf` helper para impossible.

**`static/js/view_source.js`**: `openViewSource(module, level)` → `fetch('/source/'+mod+'/'+lvl)` → injeta em modal → `Prism.highlightElement` se disponível; fallback `textContent` sem highlight (offline). Tratamento 404.

### 8.5. Componentes, formulários, interações

- Cada lab tem 1 form principal (`POST` mesma URL) + 1 level switcher + 1 View Source trigger. Exemplo SQLi: input `username`, `password`, submit; resultado tabela ou "Login failed".
- Interações sem reload total onde didático (XSS DOM lê `location.hash` 100% client-side).
- Todos os forms `method="POST"` com `autocomplete="off"` nos labs de auth; `enctype="multipart/form-data"` no upload.

### 8.6. Comunicação com backend

- Forms clássicos (`application/x-www-form-urlencoded`, `multipart` no upload) + `fetch` JSON para `/level` (Accept JSON), `/source` (JSON), `/api/*` (JSON).
- Nenhum WebSocket, nenhum GraphQL, nenhum polling.

### 8.7. Responsividade e organização

- Mobile-first mínimo: grid `repeat(auto-fill, minmax(280px,1fr))`; modal `max-width:90vw`; tabelas com `overflow-x:auto`.
- Organização fixa: `static/css/`, `static/js/`, `static/uploads/`; `templates/modules/` espelha `modules/`.

---

## 9. Docker

### 9.1. Estado atual

**Nada existe**: sem `Dockerfile`, sem `docker-compose.yml`, sem `entrypoint.sh`, sem `.dockerignore`, sem `data/`. Impossível executar o projeto hoje por qualquer meio.

### 9.2. Estrutura Docker especificada (contrato a implementar exatamente)

**`Dockerfile`** (a criar):

```dockerfile
# Especificação normativa — Próximo DESENVOLVEDOR implementa e testa
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
EXPOSE 2300
ENTRYPOINT ["./entrypoint.sh"]
```

**`docker-compose.yml`** (a criar):

```yaml
# Especificação normativa
services:
  duno-app:
    build: .
    container_name: duno-app
    ports:
      - "2300:2300"
    volumes:
      - ./data:/app/data
    environment:
      - SECRET_KEY=${SECRET_KEY:-duno-lab-secret-change-me}
      - FLASK_ENV=production
    restart: unless-stopped
```

**`entrypoint.sh`** (a criar, LF, `chmod +x`):

```bash
#!/bin/sh
set -e
echo "======================================"
echo " DUNO — Designed Unsecure Network Operations"
echo " http://localhost:2300"
echo "======================================"
if [ ! -f /app/data/duno.db ]; then
  echo "[*] Banco não encontrado, executando seed..."
  python seed.py
else
  echo "[*] Banco encontrado em /app/data/duno.db"
fi
echo "[*] Módulos: 20 | Níveis: low/medium/high/impossible"
exec python run.py
```

- **Imagens**: uma (`duno-app` build local, base `python:3.11-slim`).
- **Containers**: um (`duno-app`).
- **Portas**: `2300:2300` (host:container). Flask deve bindar `0.0.0.0:2300`.
- **Volumes**: `./data:/app/data` (bind; persiste `duno.db` + `uploads`? Decidir: uploads em `static/uploads` dentro da imagem é efêmero; recomendação: montar também `./static/uploads:/app/static/uploads` ou mover uploads para `/app/data/uploads` com symlink — documentar decisão na implementação).
- **Networks**: default bridge do Compose (sem custom).
- **Variáveis**: `SECRET_KEY` (única obrigatória), `FLASK_ENV`, `DATABASE_PATH` opcional. Fornecer `.env.example`.
- **Persistência SQLite**: arquivo `data/duno.db` no host; nunca commitar o `.db`.
- **Inicialização**: build → entrypoint banner → seed condicional → Flask. Logs devem exibir URL, módulos, níveis, tecnologia (exigência `DEPLOYMENT.md`).

### 9.3. Problemas e melhorias necessárias (para a Próximo DESENVOLVEDOR)

| # | Problema | Severidade | Ação futura |
|---|---|---|---|
| DOK-1 | Arquivos inexistentes — zero executabilidade | Crítica | Criar os 3 arquivos + `.dockerignore` + `data/.gitkeep` (Fase 0) |
| DOK-2 | `entrypoint.sh` com risco CRLF no Windows | Alta | Salvar com LF, adicionar `.gitattributes (*.sh text eol=lf)`, ou `RUN sed -i 's/\r$//'` |
| DOK-3 | Uploads efêmeros se em `static/uploads` sem volume | Média | Montar volume ou mover para `/app/data/uploads` |
| DOK-4 | Sem `healthcheck`, sem `restart`, sem `user` | Baixa/Média | Adicionar `healthcheck: test: ["CMD","curl","-f","http://localhost:2300/"]`, `restart: unless-stopped`; rodar como non-root opcional (pode quebrar labs Command Injection que esperam shell — documentar e manter root no lab) |
| DOK-5 | `SECRET_KEY` default fraca | Média (aceitável em lab, mas documentar) | `.env.example` + aviso `SECURITY.md`; nunca commitar `.env` real |
| DOK-6 | Sem `.dockerignore` | Baixa | Excluir `data/*.db`, `__pycache__`, `.git`, `*.md` pesados? Manter docs na imagem para File Inclusion lab? Decidir: File Inclusion lab lê arquivos do projeto — manter allowlist, não excluir código da imagem |

---

## 10. Documentação existente

### 10.1. Inventário (todos lidos integralmente)

| Arquivo | Linhas aprox. | Conteúdo | Avaliação |
|---|---|---|---|
| `README.md` | 239 | Visão, stack, 20 módulos+rotas, endpoints globais, árvore, porta 2300, volume, links docs | **Correta e canônica**. Referência principal. Sem código, mas consistente |
| `docs/ARCHITECTURE.md` | 218 | Monolito, core 6 arquivos, padrão Blueprint+source/, View Source via importlib/inspect, templates/static, porta | **Correta**. Base arquitetural a seguir à risca |
| `docs/DATABASE.md` | 150 | 7 tabelas com DDL, persistência, seed/reset | **Correta mas incompleta**: sem índices, sem FK completas, sem seeds concretos, sem migração |
| `docs/MODULES.md` | 106 | Catálogo 20 módulos, rotas, estrutura, fluxo, JWT/IDOR/rate no API | **Correta, superficial**: sem comportamento por nível; Próximo DESENVOLVEDOR deve detalhar por módulo |
| `docs/DEPLOYMENT.md` | 164 | Docker-only, comandos, entrypoint, troubleshooting, isolamento | **Correta**. Falta `.env`, healthcheck, uploads |
| `docs/DEVELOPMENT.md` | 160 | Padrão módulo, rotas esperadas, frontend Vanilla, Prism CDN, checklist 18 itens | **Correta e acionável**. Checklist deve virar DoD por módulo |
| `docs/BUILD_GUIDE.md` | 189 | Identidade, stack, system prompt, prompt de geração de módulo, política de arquivos | **Correta**. Contém prompts prontos para a Próximo DESENVOLVEDOR reutilizar |
| `docs/ROADMAP.md` | 135 | Fases 0–9, 20 dias estimados | **Correta como plano**, mas fases 5/6 sobrepõem API Versioning/Mass Assignment (ver contradição) |
| `docs/SECURITY.md` | 84 | Natureza vulnerável, Docker-only, porta, uploads, reset, uso responsável | **Correta**. Deve ser preservada e exibida no dashboard |
| `docs/SECURITY_LEVELS.md` | 121 | Semântica low/medium/high/impossible, persistência, endpoints | **Correta**. Exemplos conceituais (prepared+falha sessão) devem guiar high |
| `LICENSE` | 21 | MIT 2026 Dione Lima | **Correta**. Manter |

### 10.2. Documentação correta

Toda a documentação de intenção (arquitetura, rotas, tabelas, níveis, deploy) é coerente entre si e suficiente como especificação para construção. Não há código para contradizê-la.

### 10.3. Documentação desatualizada / ausente

- Nenhum doc descreve `config.py`, `requirements.txt`, `.env`, comportamento exato de `reset` (preserva users?), autenticação (rotas protegidas?), rate limit, JWT secrets, Swagger.
- Nenhum diagrama de sequência por módulo; nenhum exemplo de request/response.
- Nenhum guia de testes; nenhum `CHANGELOG`.

### 10.4. Contradições identificadas

1. **API Versioning + Mass Assignment duplicados**: aparecem como módulos web 18–19 (`/api_versioning`, `/mass_assignment`) **e** como itens da Fase 6 API Security. Risco de implementação dupla/divergente. **Resolução neste plano**: implementar 18–19 como labs web (form/JSON) **e** replicar os conceitos dentro de `/api/*` (endpoints versionados + mass assignment JSON), documentando a sobreposição como intencional-didática.
2. **Contagem de módulos**: README diz "19 + 1 especial" = 20 rotas; MODULES lista 20 linhas numeradas 1–20 (19 web + API). Consistente, mas fraseado de forma ambígua. **Resolver**: tratar sempre como 20 entradas.
3. **`FINAL_PLAN.md` vs `PLANO_FINAL.md`**: a tarefa pede `FINAL_PLAN.md` no objetivo e `PLANO_FINAL.md` no corpo. **Resolução**: este arquivo é `FINAL_PLAN.md` (nome do objetivo); mencionar o alias no cabeçalho.
4. **Swagger UI**: ROADMAP Fase 6 cita Swagger UI sem stack definida (sem `flask-swagger-ui` no stack). **Resolução**: implementar `/api/docs` como página estática documentando endpoints (sem dependência nova) ou adicionar `flask-swagger-ui` com decisão explícita.

### 10.5. O que precisa ser atualizado (pela Próximo DESENVOLVEDOR, não agora)

- Atualizar `README.md` somente se rotas/portas/volume mudarem (não devem).
- Criar `docs/API.md` (contrato `/api/*`), `docs/TESTING.md` (como validar), `CHANGELOG.md` (opcional).
- Manter demais docs intactos salvo mudança arquitetural real.

---

## 11. Estado atual do projeto

### 11.1. Implementado (funciona ou está presente)

- ✅ Especificação escrita (9 docs + README + LICENSE). Qualidade: boa, consistente, suficiente para construir.
- ✅ Identidade, stack, arquitetura, catálogo de módulos/rotas, DDL das tabelas, semântica dos níveis, regras Docker, checklist de módulo, prompts de geração.
- ❌ Nada mais. Nenhum comportamento executável.

### 11.2. Parcialmente implementado

- **Nada** se qualifica como parcial — não há código incompleto, TODO, placeholder ou stub. Verificação por `Get-ChildItem -Recurse` confirma ausência total. (Não há código duplicado ou complexo — não há código.)

### 11.3. Não implementado (tudo — lista exaustiva para a Próximo DESENVOLVEDOR)

- Fundação: `Dockerfile`, `docker-compose.yml`, `entrypoint.sh`, `requirements.txt`, `.dockerignore`, `.gitignore`, `.env.example`, `data/.gitkeep`.
- Núcleo Python: `run.py`, `config.py`, `seed.py`, `app.py`, `core/__init__.py`, `core/database.py`, `core/security_levels.py`, `core/reset.py`, `core/source_loader.py`, `core/auth.py`, `core/decorators.py`.
- Rotas globais: `/`, `/login`, `/logout`, `/level/<module>`, `/source/<module>/<level>`, `/reset`, handlers 404/500.
- 20 módulos × (`__init__`, `routes`, `logic`, `source/low|medium|high|impossible`) = ~140 arquivos Python.
- Templates: `base`, `index`, `login`, 2 partials, 20 labs = ~25 HTML.
- Static: `duno.css`, `duno.js`, `view_source.js`, `uploads/.gitkeep`.
- Banco: arquivo `duno.db`, seeds, índices, migração.
- Testes, docs complementares (`API.md`, `TESTING.md`).

### 11.4. Problemas encontrados

1. **Ausência total de implementação** — o projeto não executa, não responde, não persiste. Qualquer comando `docker-compose up` falha (arquivos inexistentes).
2. **Sem validação possível hoje** — não há como testar rotas, níveis, View Source, reset, Docker, segurança.
3. **Lacunas de especificação** (detalhes que a Próximo DESENVOLVEDOR terá que decidir e documentar): comportamento exato de auth/reset, contrato JSON da API, JWT secrets, rate limit, Swagger, uploads persistentes, migração de schema.
4. **Risco de divergência futura View Source vs. lógica** — mitigado pelo padrão `logic` importa `source` (Seção 4.3).
5. **Risco de ambiente Windows/CRLF** para `entrypoint.sh`.
6. **Nenhum controle de segredos/`.gitignore`** — risco de commitar `duno.db` ou `.env` quando criados.

---

## 12. Análise de segurança

> Escopo: exclusivamente código/ambiente **deste projeto**. Nenhum sistema externo foi tocado. Como não há código, a análise é sobre **(a)** vulnerabilidades **intencionais** que deverão existir (didáticas) e **(b)** vulnerabilidades **não-intencionais** que a implementação deverá evitar fora dos labs.

### 12.1. Vulnerabilidades intencionais (didáticas — IMPLEMENTAR de propósito, isoladas por nível `low`)

Cada módulo `low` deve ser explorável conforme OWASP Top 10 / API Top 10. Isso **não** é defeito — é requisito. Obrigações:

- Isolar a falha ao módulo/nível (não vazar para `core` ou outros módulos).
- Comentar `<!-- INTENTIONALLY VULNERABLE (low) — training only -->` nos pontos propositais.
- Garantir que `impossible` fecha a falha com controle real (prepared, escape, token, allowlist, JWT verify, etc.).
- Exibir aviso global "deliberadamente vulnerável — uso local apenas".

### 12.2. Superfície não-intencional (EVITAR — mesmo em lab)

| Vetor | Análise atual | Exigência futura |
|---|---|---|
| Autenticação | Inexistente; seed `admin/password` pública | Hash `werkzeug.security` (scrypt/pbkdf2), sessão Flask assinada, `SECRET_KEY` via env, logout limpa sessão, erro de login genérico em `high/impossible` |
| Autorização | Sem decoradores | `@login_required` global; `@admin_required` no `auth_bypass` impossible; IDOR fechado via `session user_id == resource owner` |
| Sessões/Cookies | Sem config | `SESSION_COOKIE_HTTPONLY=True`, `SAMESITE=Lax` (lab CSRF manipula por rota em low), `Secure` quando HTTPS; `PERMANENT_SESSION_LIFETIME` curto; IDs `secrets.token_urlsafe` em impossible |
| CSRF | Lab próprio; switcher global e reset são alvos | `POST` + token criptográfico para `/level`, `/reset`, forms sensíveis em `high/impossible`; low permite bypass didático **somente dentro do lab `/csrf`** |
| XSS | 3 labs + guestbook | Escape padrão Jinja2 em tudo exceto XSS-low intencional; `CSP` base em impossible; `HttpOnly` nos cookies |
| SQL Injection | 2 labs | `sqlite3` com `?` placeholders em todo `core` e em `high/impossible` dos labs; concatenação **somente** em `low/medium` dos labs SQLi, via conexão central |
| Validação de entrada | Inexistente | Allowlist + tipos + tamanhos em impossible; `MAX_CONTENT_LENGTH`; `ipaddress`, `safe_join`, `urllib.parse` para redirect/inclusion |
| Sanitização | Inexistente | `html.escape` / Jinja autoescape; nunca `|safe` fora dos labs XSS-low |
| Exposição de informações | Risco View Source/`debug` | `debug=False`, handlers 404/500 sem traceback, View Source com whitelist (nunca path cru), sem `.git`/`​.env` servidos |
| Secrets | Nenhum ainda | `SECRET_KEY`, JWT secret, Fernet key via env + `.env.example`; nunca hardcoded em repo; `cryptography` lab usa chave efêmera documentada |
| Docker | Sem arquivos | Não expor 2300 à Internet; `restart` + `healthcheck`; imagem `slim`; `pip --no-cache`; non-root se não quebrar labs shell (documentar escolha) |
| Dependências | Sem lock | Pinar versões em `requirements.txt`; `pip audit` manual antes de fechar |
| Uploads | Dir inexistente | Allowlist + magic bytes + rename + `MAX_CONTENT_LENGTH` em impossible; servir sem execução (`X-Content-Type-Options: nosniff`); reset limpa |
| Controle de acesso | Sem RBAC | `role` em sessão server-side (nunca cookie client confiado); `auth_bypass` lab demonstra o erro em low |
| Tratamento de erros | Inexistente | Try/except didático nos labs; 500 genérico fora dos labs |

### 12.3. Nota sobre testes de segurança

A Próximo DESENVOLVEDOR validará exploração **somente contra `http://localhost:2300` local** (próprio container). Nenhum teste contra terceiros. Cada lab deve ter PoC manual documentada (ex.: `' OR '1'='1`, `<script>alert(1)</script>`, `;id`, `../../etc/passwd`, JWT `none`) restrita ao ambiente lab.

---

## 13. Problemas e prioridades

| ID | Problema | Prioridade | Motivo |
|---|---|---|---|
| P-CRIT-1 | Zero executabilidade (sem Dockerfile/Compose/entrypoint/requirements/código) | **Crítico** | Nada funciona; bloqueia tudo |
| P-CRIT-2 | Sem `seed.py`/`duno.db`/schema | **Crítico** | Sem banco, auth/levels/labs falham |
| P-CRIT-3 | Sem `core` (db, levels, source, auth, reset) | **Crítico** | Sem núcleo, nenhum módulo opera |
| P-ALT-1 | Sem 20 módulos (140 arquivos) | **Alto** | Coração do laboratório ausente |
| P-ALT-2 | Sem templates/static (frontend zero) | **Alto** | Sem UI, sem interação, sem View Source visual |
| P-ALT-3 | Sem `run.py`/`app.py`/`config.py` (Flask não inicia) | **Alto** | Sem app, sem rotas |
| P-ALT-4 | Risco CRLF `entrypoint.sh` no Windows | **Alto** | Container não inicia se CRLF |
| P-ALT-5 | Contradição API Versioning/Mass Assignment (web vs API) | **Alto** | Risco de dupla implementação divergente |
| P-MED-1 | Sem índices/FK completas/migração | **Médio** | Performance/integridade futuras |
| P-MED-2 | Uploads sem persistência definida | **Médio** | Perda de arquivos / execução indesejada |
| P-MED-3 | Sem contrato `/api/*` detalhado (JWT, IDOR, rate, docs) | **Médio** | API é o módulo mais complexo e vago |
| P-MED-4 | Sem `.gitignore`/`.env.example`/secrets policy | **Médio** | Risco de vazar `.db`/segredos |
| P-MED-5 | Prism via CDN sem fallback offline | **Médio** | View Source ilegível offline |
| P-BAI-1 | Sem healthcheck/restart/logs padronizados | **Baixo** | Operação, não função |
| P-BAI-2 | Sem testes automatizados | **Baixo** | Lab é manual por natureza; testes são validação, não entrega core |
| P-BAI-3 | Docs complementares ausentes (`API.md`, `TESTING.md`) | **Baixo** | Documentação, pós-funcional |

---

## 14. Plano de implementação futuro

> **Não implementar agora.** Cada tarefa abaixo é para a Próximo DESENVOLVEDOR. Campos obrigatórios por tarefa: ID, prioridade, arquivos, objetivo, alteração, como implementar, dependências, impacto, critérios de conclusão, como testar.

### FASE 0 — Fundação Docker + esqueleto (pré-requisito de tudo)

**T-001 — Criar `requirements.txt`**
- Prioridade: Crítica. Arquivos: `requirements.txt` (criar).
- Objetivo: fixar dependências Python 3.11 + Flask 3.x.
- Alteração: criar com `Flask==3.1.0, Werkzeug==3.1.3, Jinja2==3.1.4, itsdangerous==2.2.0, click==8.1.7, PyJWT==2.10.1, cryptography==44.0.0, gunicorn==23.0.0`.
- Como: escrever arquivo, sem instalar local (validação via Docker).
- Dependências: nenhuma. Impacto: base do build.
- Conclusão: `pip install -r requirements.txt` passa dentro do build.
- Teste: `docker build -t duno-test .` (após T-002) ou `pip check` no container.

**T-002 — Criar `Dockerfile` + `.dockerignore`**
- Prioridade: Crítica. Arquivos: `Dockerfile`, `.dockerignore` (criar).
- Objetivo: imagem `python:3.11-slim` que instala deps e expõe 2300.
- Como: conforme especificação §9.2; `.dockerignore` com `__pycache__/`, `*.pyc`, `data/*.db`, `.git/`, `.env`.
- Dependências: T-001. Impacto: build.
- Conclusão: `docker build` sucede.
- Teste: `docker build -t duno-app .` sem erro.

**T-003 — Criar `docker-compose.yml` + `.env.example` + `.gitignore`**
- Prioridade: Crítica. Arquivos: `docker-compose.yml`, `.env.example`, `.gitignore` (criar).
- Objetivo: serviço único `duno-app`, `2300:2300`, volume `./data:/app/data`.
- Como: YAML §9.2; `.env.example` com `SECRET_KEY=duno-lab-secret-change-me`; `.gitignore` com `data/*.db`, `.env`, `__pycache__/`.
- Dependências: T-002. Impacto: `up` possível.
- Conclusão: `docker compose config` valida.
- Teste: `docker-compose config` / `docker compose config` sem erro.

**T-004 — Criar `entrypoint.sh` (LF) + `data/.gitkeep` + `static/uploads/.gitkeep`**
- Prioridade: Crítica. Arquivos: `entrypoint.sh`, `data/.gitkeep`, `static/uploads/.gitkeep` (criar).
- Objetivo: banner + seed condicional + `exec python run.py`.
- Como: script §9.2, salvar **LF**, `chmod +x`; adicionar `.gitattributes` com `*.sh text eol=lf`.
- Dependências: T-003. Impacto: inicialização.
- Conclusão: container inicia e exibe banner.
- Teste: `docker-compose up --build` mostra banner (após Fase 1 para seed completo).

**T-005 — Criar `config.py` + `run.py` + `app.py` (factory mínima + `/` placeholder)**
- Prioridade: Alta. Arquivos: `config.py`, `run.py`, `app.py` (criar).
- Objetivo: Flask inicia em `0.0.0.0:2300` com dashboard placeholder.
- Como: `config.py` (SECRET_KEY env, DATABASE `/app/data/duno.db`, UPLOAD_FOLDER, MAX_CONTENT_LENGTH=2MB); `app.py:create_app()` com 1 rota `/` retornando "DUNO bootstrapping"; `run.py` chama `create_app().run(host,port)`.
- Dependências: T-001–T-004. Impacto: primeiro `up` verde.
- Conclusão: `http://localhost:2300/` responde 200.
- Teste: `curl -s -o /dev/null -w "%{http_code}" http://localhost:2300/` → `200`; `docker-compose logs` sem traceback.

### FASE 1 — Core + Banco + Recursos globais

**T-010 — Criar `core/database.py` + `seed.py` (DDL + seeds)**
- Prioridade: Crítica. Arquivos: `core/__init__.py`, `core/database.py`, `seed.py` (criar).
- Objetivo: SQLite inicializável com 7 tabelas + índices + seeds.
- Como: implementar `get_db/close_db/init_db/query_db`; `seed.py` com DDL §7.2 + `CREATE INDEX` §16 + inserts (`admin/password` admin, `user/password` user, secrets demo, captcha demo, api_tokens demo) com `INSERT OR IGNORE`; `PRAGMA foreign_keys=ON`.
- Dependências: T-005. Impacto: todo o resto.
- Conclusão: `python seed.py` cria `data/duno.db` com 7 tabelas e seeds; re-execução idempotente.
- Teste: `sqlite3 data/duno.db ".tables"` lista 7; `SELECT * FROM users;` mostra admin; segunda execução não duplica.

**T-011 — Criar `core/security_levels.py` + `POST /level/<module>`**
- Prioridade: Crítica. Arquivos: `core/security_levels.py`, `app.py` (alterar: registrar rota).
- Objetivo: persistir nível por (user, módulo).
- Como: `get_level(user_id, module)->str` (default `low`), `set_level(user_id, module, level)` com validação whitelist + UPSERT; rota `POST /level/<module>` lê `request.form["level"]` ou JSON, exige login, redirect ou JSON.
- Dependências: T-010 + T-012 (auth para user_id; usar fallback `user_id=1` temporário até auth pronto, depois migrar).
- Conclusão: trocar nível persiste após restart (volume).
- Teste: `curl -X POST -d "level=high" http://localhost:2300/level/sqli -b cookie` → 302; `sqlite3` mostra linha; nível inválido → 400.

**T-012 — Criar `core/auth.py` + `core/decorators.py` + `/login` `/logout`**
- Prioridade: Alta. Arquivos: `core/auth.py`, `core/decorators.py`, `templates/login.html`, `app.py` (alterar).
- Objetivo: login lab funcional.
- Como: `authenticate()` com `check_password_hash`, `session["user_id"]`, `@login_required` (redirect `/login`), seeds hash via `generate_password_hash`; template form simples.
- Dependências: T-010. Impacto: protege todas as rotas.
- Conclusão: `admin/password` loga, sessão persiste, `/logout` limpa, rota protegida sem login → redirect.
- Teste: manual login/logout + `curl` sem cookie → 302 `/login`.

**T-013 — Criar `core/source_loader.py` + `GET /source/<module>/<level>`**
- Prioridade: Alta. Arquivos: `core/source_loader.py`, `app.py` (alterar).
- Objetivo: View Source fiel via importlib/inspect.
- Como: whitelist `ALLOWED_MODULES` (20) + `ALLOWED_LEVELS` (4); `importlib.import_module(f"modules.{mod}.source.{lvl}")` + `inspect.getsource`; retorna JSON `{module, level, code}`; 404 fora da whitelist.
- Dependências: T-005 (módulos ainda placeholder; testar com 1 módulo dummy, depois validar com todos na Fase 3–6).
- Conclusão: `/source/sqli/low` retorna código 200 JSON.
- Teste: `curl http://localhost:2300/source/sqli/low` → JSON com `code`; `/source/xxx/low` → 404.

**T-014 — Criar `core/reset.py` + `POST /reset`**
- Prioridade: Alta. Arquivos: `core/reset.py`, `app.py` (alterar).
- Objetivo: restaurar dados de lab preservando users/levels.
- Como: `reset_lab_data()` deleta `guestbook`, `captcha_challenges`, `audit_log`, reseta `secrets`/`api_tokens` demo via re-seed parcial; preserva `users` + `security_levels`; rota POST exige login.
- Dependências: T-010. Impacto: todos os labs.
- Conclusão: inserir guestbook → POST /reset → guestbook vazio, users intactos.
- Teste: `INSERT INTO guestbook...` → `curl -X POST /reset` → `SELECT COUNT` = seed count.

### FASE 2 — Interface base

**T-020 — Criar `templates/base.html` + `static/css/duno.css` + `templates/index.html` (dashboard 20 cards)**
- Prioridade: Alta. Arquivos: `templates/base.html`, `templates/index.html`, `static/css/duno.css` (criar).
- Objetivo: layout + dashboard navegável.
- Como: base com nav + blocos + footer aviso vulnerável; index com loop de 20 módulos (passar lista de `app.py`); CSS dark responsivo.
- Dependências: T-005, T-012. Impacto: base de todos os templates.
- Conclusão: `/` exibe 20 cards com links corretos.
- Teste: abrir `http://localhost:2300/`, contar 20 cards, clicar cada link → 200 ou placeholder documentado.

**T-021 — Criar partials `_level_switch.html`, `_view_source_modal.html` + `static/js/duno.js`, `static/js/view_source.js`**
- Prioridade: Alta. Arquivos: 2 partials + 2 JS (criar); `base.html` (alterar: incluir).
- Objetivo: troca de nível + modal View Source funcionais sem framework.
- Como: form POST + `fetch` progressive; modal fetch `/source`; Prism CDN com fallback.
- Dependências: T-011, T-013, T-020. Impacto: todos os labs.
- Conclusão: trocar nível via UI persiste; modal exibe código com highlight.
- Teste: manual UI + DevTools Network 200; offline (bloquear CDN) ainda exibe texto.

### FASE 3 — Módulos 1–6 (Brute Force → CAPTCHA)

Para cada módulo M em [brute_force, command_injection, csrf, file_inclusion, file_upload, captcha], repetir o padrão (exemplo T-030 para brute_force; demais T-031…T-035 idênticos em estrutura):

**T-030 — Implementar `brute_force` (modelo para todos)**
- Prioridade: Alta. Arquivos: `modules/brute_force/__init__.py`, `routes.py`, `logic.py`, `source/low|medium|high|impossible.py`, `templates/modules/brute_force.html` (criar); `app.py` (alterar: `register_blueprint`).
- Objetivo: lab funcional nos 4 níveis + View Source fiel + level + reset.
- Como: seguir §6.2 comportamento por nível; `logic.dispatch`; `routes` integra `get_level`; template com form + `_level_switch` + botão View Source; `source/*.py` espelha `logic`.
- Dependências: T-010–T-021. Impacto: isolado (só este módulo).
- Conclusão: checklist DEVELOPMENT.md 18 itens marcados para este módulo.
- Teste: manual por nível (low explorável, impossible bloqueia) + `/source/brute_force/<lvl>` 200 + troca de nível persiste + reset limpa audit.

Demais: **T-031 command_injection, T-032 csrf, T-033 file_inclusion, T-034 file_upload, T-035 captcha** — mesma estrutura, prioridade Alta, mesmos critérios. Notas específicas:
- `file_upload`: exige `MAX_CONTENT_LENGTH`, `static/uploads/` + volume (ver §17).
- `captcha`: exige `captcha_challenges` + flag `used`.
- `csrf`: o próprio lab demonstra ausência de token em low; o switcher global **não** deve ser vulnerável — documentar separação.

### FASE 4 — Módulos 7–12 (SQLi → XSS Stored)

**T-040 sqli, T-041 sqli_blind, T-042 weak_session, T-043 xss_dom, T-044 xss_reflected, T-045 xss_stored** — Prioridade Alta, mesma estrutura T-030.
- Notas: `sqli*` usam `users` + concatenação apenas em low/medium; `xss_stored` usa `guestbook`; `xss_dom` é majoritariamente JS (`location.hash`); `weak_session` manipula cookies/sessão didática (não quebrar sessão real do Flask — usar cookie separado `duno_sid` para o lab).

### FASE 5 — Módulos 13–19 (CSP → Mass Assignment)

**T-050 csp_bypass, T-051 js_attacks, T-052 auth_bypass, T-053 open_redirect, T-054 crypto, T-055 api_versioning, T-056 mass_assignment** — Prioridade Alta, mesma estrutura.
- Notas: `crypto` requer `PyJWT`/`cryptography` apenas aqui; `api_versioning`/`mass_assignment` web devem ser compatíveis com os endpoints `/api/*` (documentar sobreposição intencional, §10.4).

### FASE 6 — API Security (`/api/*`)

**T-060 — Implementar `modules/api_security` + `templates/modules/api_security.html` + `docs/API.md`**
- Prioridade: Alta. Arquivos: `modules/api_security/*` (7 arquivos), template, `docs/API.md` (criar).
- Objetivo: laboratório JSON com JWT, IDOR, rate limit, versionamento, mass assignment.
- Como: Blueprint `url_prefix="/api"`; endpoints `POST /api/login` (emite JWT), `GET /api/users/<id>` (IDOR lab), `GET /api/secrets` (version header), `POST /api/users` (mass assignment), `GET /api/docs` (doc estática); níveis controlam verificação JWT (`none`→secret fraco→sem exp→verify), checagem owner, rate (ausente→audit).
- Dependências: T-010 (api_tokens/users), T-011–T-014. Impacto: maior complexidade; isolado em `/api`.
- Conclusão: 4 níveis exploráveis via `curl`; docs com exemplos de request/response.
- Teste: `curl` por nível (JWT none aceito em low, rejeitado em impossible; IDOR possível em low, bloqueado em impossible; rate/burst).

### FASE 7 — Seed final, reset global, hardening lab, docs

**T-070 — Revisar `seed.py` + `reset.py` + migração `PRAGMA user_version`**
- Prioridade: Média. Arquivos: `seed.py`, `core/reset.py` (alterar).
- Objetivo: seeds determinísticos + reset documentado + migração incremental.
- Como: `user_version` bump por mudança DDL; `migrate()` aplica ALTERs; reset preserva users/levels.
- Dependências: todas as fases de módulos. Impacto: banco existente no volume.
- Conclusão: `rm data/duno.db` + `up` recria tudo; reset não desloga.
- Teste: popular labs → reset → verificar preservação + idempotência.

**T-071 — hardening não-lab (cookies, headers, erros, SECRET_KEY)**
- Prioridade: Média. Arquivos: `config.py`, `app.py` (alterar).
- Objetivo: fechar superfície fora dos labs (§12.2).
- Como: `HTTPONLY`, `SAMESITE`, `debug=False`, handlers 404/500, `nosniff`, CSP base (exceto rota `csp_bypass` low).
- Dependências: T-070. Conclusão: headers verificáveis, sem traceback.
- Teste: `curl -i` inspeciona `Set-Cookie`, `Content-Security-Policy`; 404 custom.

**T-072 — Documentação complementar (`docs/API.md`, `docs/TESTING.md`, README se necessário)**
- Prioridade: Baixa. Arquivos: `docs/API.md`, `docs/TESTING.md` (criar); `README.md` (alterar só se rota/porta mudar — não deve).
- Objetivo: próxima operadora entende API e validação sem ler código.
- Como: exemplos curl por módulo/nível; matriz de testes.
- Dependências: T-060. Conclusão: docs espelham implementação.
- Teste: seguir `TESTING.md` do zero e obter verde.

---

## 15. Alterações por arquivo

### 15.1. Criados (Próximo DESENVOLVEDOR — lista normativa completa)

| Arquivo(s) | Motivo |
|---|---|
| `Dockerfile` | Imagem única `python:3.11-slim`, porta 2300. Sem ele, nada executa (P-CRIT-1) |
| `docker-compose.yml` | Serviço `duno-app`, volume `./data:/app/data`. Sem ele, sem orquestração |
| `.dockerignore` | Evitar `duno.db`/pycache na imagem |
| `.gitignore` | Não versionar `data/*.db`, `.env`, pycache |
| `.gitattributes` | Forçar `*.sh eol=lf` (risco CRLF Windows) |
| `.env.example` | Documentar `SECRET_KEY` sem vazar segredo |
| `entrypoint.sh` | Banner + seed condicional + Flask |
| `requirements.txt` | Pinar Flask 3.x + JWT + crypto + gunicorn |
| `run.py` | Entrypoint Python (`0.0.0.0:2300`) |
| `config.py` | Centralizar env, DB path, uploads, limites |
| `app.py` | Factory + registro Blueprints + rotas globais + handlers erro |
| `seed.py` | DDL 7 tabelas + índices + seeds idempotentes |
| `data/.gitkeep`, `static/uploads/.gitkeep` | Manter dirs vazios versionados |
| `core/__init__.py`, `database.py`, `security_levels.py`, `reset.py`, `source_loader.py`, `auth.py`, `decorators.py` | Núcleo transversal (P-CRIT-3) |
| `modules/*/__init__.py`, `routes.py`, `logic.py`, `source/low|medium|high|impossible.py` (×20 = ~140 arquivos) | 20 labs × 4 níveis (P-ALT-1) |
| `templates/base.html`, `index.html`, `login.html`, `_level_switch.html`, `_view_source_modal.html`, `modules/*.html` (×20) | UI completa (P-ALT-2) |
| `static/css/duno.css`, `static/js/duno.js`, `static/js/view_source.js` | Frontend Vanilla |
| `docs/API.md`, `docs/TESTING.md` | Contrato API + guia de validação |
| `FINAL_PLAN.md` | Este arquivo (já criado nesta etapa; preservar) |

### 15.2. Alterados (Próximo DESENVOLVEDOR)

| Arquivo | Motivo da alteração futura |
|---|---|
| `app.py` | A cada módulo: adicionar `register_blueprint`. A cada recurso global: adicionar rota |
| `config.py` | Ajustar limites/cookies/headers após hardening (T-071) |
| `seed.py`, `core/reset.py` | Refinar seeds/migração após todos os módulos (T-070) |
| `templates/base.html` | Incluir novos JS/CSS se criados; nunca quebrar blocos |
| `README.md`, demais `docs/` | Somente se arquitetura/rotas/portas mudarem de verdade; caso contrário, não tocar |

### 15.3. Removidos

- **Nenhum arquivo existente deve ser removido.** `LICENSE`, `README.md`, `docs/*.md` e este `FINAL_PLAN.md` são preservados. `.db` gerado nunca é "removido" pelo código — apenas recriado via reset documentado.

### 15.4. Mantidos sem alteração (nesta etapa e como regra)

- `LICENSE` — intocado.
- `README.md` — intocado nesta análise; alteração futura só por necessidade real.
- `docs/ARCHITECTURE.md`, `DATABASE.md`, `MODULES.md`, `DEPLOYMENT.md`, `DEVELOPMENT.md`, `BUILD_GUIDE.md`, `ROADMAP.md`, `SECURITY.md`, `SECURITY_LEVELS.md` — intocados; são a especificação canônica.

---

## 16. Banco de dados — alterações futuras

> Nenhuma alteração executada agora. Arquivo `.db` não criado, nenhuma query rodada.

### 16.1. DDL base (usar §7.2 como ponto de partida)

### 16.2. Alterações normativas a aplicar na criação

```sql
-- FK faltantes (DB-2)
-- Em api_tokens e audit_log, adicionar:
FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE

-- Índices (DB-3) — criar em seed.py após DDL:
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_levels_user_module ON security_levels(user_id, module);
CREATE INDEX IF NOT EXISTS idx_tokens_token ON api_tokens(token);
CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_log(ts);
CREATE INDEX IF NOT EXISTS idx_captcha_used ON captcha_challenges(used);

-- PRAGMAs (em database.py ao conectar):
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

### 16.3. Tabelas/campos novos vs. removidos

- **Novos**: nenhum obrigatório. Opcional: `uploads(id, filename, stored_as, mime, size, user_id, ts)` para rastrear File Upload (decidir na T-034; se criado, documentar em `DATABASE.md`).
- **Removidos**: nenhum. Não remover colunas documentadas.
- **Tipos**: manter `TEXT/INTEGER/TIMESTAMP`; não introduzir `BOOLEAN` (usar `INTEGER 0/1` para `used`).

### 16.4. Migrações

- `seed.py` deve conter `SCHEMA_VERSION = 1` + `PRAGMA user_version`.
- Função `migrate(conn)`: lê `user_version`, aplica `ALTER TABLE ... ADD COLUMN ...` incrementais, atualiza versão.
- Reset **não** faz DDL destrutivo em `users`/`security_levels`; apenas limpa tabelas voláteis.

### 16.5. Preservação de dados

- Volume `./data:/app/data` é a única persistência. Antes de qualquer migração destrutiva: `cp data/duno.db data/duno.db.bak`.
- `POST /reset` nunca apaga `users` nem `security_levels` (decisão normativa; se a Próximo DESENVOLVEDOR escolher full-wipe, deve documentar e justificar em `docs/DATABASE.md`).
- Nunca commitar `*.db` ou `*.bak`.

---

## 17. Docker — alterações futuras

| Item | Alteração futura exata |
|---|---|
| `Dockerfile` | Criar conforme §9.2. Base `python:3.11-slim`. Não usar `latest`. `EXPOSE 2300`. `ENTRYPOINT ["./entrypoint.sh"]`. Não adicionar Postgres/Redis/Nginx |
| `docker-compose.yml` | Criar conforme §9.2. `ports: ["2300:2300"]`, `volumes: ["./data:/app/data"]`, `env SECRET_KEY`, `restart: unless-stopped`. Adicionar `healthcheck` (curl) se `curl` instalado (`RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`) ou healthcheck via `python -c urllib`. Documentar escolha |
| `entrypoint.sh` | Criar LF + `chmod +x` + banner + seed condicional + `exec python run.py`. Logar URL/módulos/níveis (exigência DEPLOYMENT.md) |
| Volumes | `./data:/app/data` obrigatório. Uploads: ou `static/uploads` dentro da imagem (efêmero, aceitável se reset limpa) **ou** mover para `/app/data/uploads` + servir via rota Flask `send_from_directory` (persistente). **Recomendação**: `/app/data/uploads` + rota, para sobreviver a rebuild. Documentar decisão |
| Networks | Manter default. Não criar custom sem motivo |
| Env | `SECRET_KEY`, `FLASK_ENV=production`, opcional `DATABASE_PATH`, `JWT_SECRET`. `.env` nunca commitado |
| Persistência SQLite | Validar: `up` → cria `data/duno.db`; `down` mantém; `down -v`? (bind não é volume nomeado — `down -v` não apaga bind; documentar). `reset` não apaga arquivo, só linhas |
| Inicialização | `docker-compose up --build` deve terminar em Flask ouvindo `0.0.0.0:2300` em <60s em máquina típica |
| Melhorias pós-MVP | `healthcheck`, `restart`, `.dockerignore`, non-root (somente se labs shell continuarem funcionando; caso contrário manter root com aviso) |

---

## 18. Frontend — alterações futuras

### 18.1. Mudanças de interface (todas são criação, não reforma)

- **Base**: nav com logo `DUNO`, links Dashboard/Login/Logout, badge usuário, botão `Reset Database` (POST com confirm), footer com aviso "Deliberadamente vulnerável — laboratório local".
- **Dashboard**: hero + grid 20 cards. Cada card: `#`, nome, descrição 1 linha (de MODULES.md), rota `code`, badge nível atual (requer leitura `security_levels` por usuário), botões Acessar + Source.
- **Labs**: título, descrição didática curta, `_level_switch`, form do lab, área resultado, dicas de exploração (collapsible `details` — sem entregar payload completo? Decidir: lab didático deve sugerir vetores, ex. "tente `' OR 1=1 --`"), botão View Source por nível.
- **Login**: form centralizado + hint `admin / password` (lab).
- **Modal**: overlay + `<pre><code class="language-python">`, seletor de nível dentro do modal, botão copiar, fechar ESC/backdrop.
- **API docs page**: tabela de endpoints + exemplos curl (se Swagger UI descartado).

### 18.2. Mudanças de comportamento (JS)

- `duno.js`: intercepta `.level-form` submit → `fetch POST` → atualiza badge sem reload (fallback: submit normal funciona sem JS); `reset` com `confirm()`; `toast()` para feedback.
- `view_source.js`: `data-vs="module:level"` → modal; cache em memória por (mod,lvl); erro 404 → toast.
- `xss_dom.html` + JS inline intencionalmente vulnerável em low (`innerHTML = location.hash.slice(1)`), seguro em impossible (`textContent`).

### 18.3. CSS

- Criar `duno.css` (~600–900 linhas): variáveis, reset, nav, hero, grid, card, badge por nível, form, input, button, table, pre/code, modal, toast, footer, `@media 768px`.
- Sem frameworks; Prism CSS via CDN opcional com fallback (pre legível sem ele).

---

## 19. Backend — alterações futuras

### 19.1. Flask / app factory

- Criar `app.py:create_app()` com config, teardown DB, registro Blueprints em loop explícito (lista `BLUEPRINTS = [...]` para ordem estável do dashboard), rotas globais, handlers 404/500, injeção de `current_user` via `g`/`context_processor`.
- `run.py` mínimo; `debug=False`; `host="0.0.0.0"`, `port=2300` (ler `PORT` env opcional, default 2300).

### 19.2. APIs / serviços / models

- `core/*` conforme §6.6. `logic.py` por módulo com funções puras + `dispatch`.
- `/api/*` como Blueprint com `url_prefix="/api"`, respostas `jsonify`, códigos corretos (200/400/401/403/404/429), `Content-Type: application/json`.
- JWT: `PyJWT`, `HS256`, `exp` 1h, secret via env; low aceita `alg=none`/sem verify (intencional, comentado); impossible `decode(..., algorithms=["HS256"], options={require exp})`.

### 19.3. Validações e erros

- Whitelist módulo/nível em `/level` e `/source`; `abort(404)` fora da lista.
- Cada `routes.py` valida tipos/tamanhos antes de chamar `logic` em `high/impossible`; `low` passa cru (intencional).
- Handlers globais: `404.html`/`500.html` (criar templates de erro simples estendendo base).

### 19.4. Segurança do próprio framework (fora dos labs)

- Ver §12.2 e T-071. Nenhuma falha global além das isoladas nos labs `low`.

---

## 20. Testes

> Nenhum teste executado nesta etapa (nada para testar). Abaixo, o protocolo que a Próximo DESENVOLVEDOR deve seguir. Nenhum teste toca sistemas externos; tudo contra `http://localhost:2300` local.

### 20.1. Testes funcionais (manuais, por módulo — repetir para os 20)

Para cada módulo/nível (`low|medium|high|impossible`):

1. `up` limpo, login `admin/password`, abrir `/<rota>` → 200, form visível, nível default `low`.
2. Executar caso benigno (ex. SQLi login válido, XSS texto normal, upload `.png`) → sucesso.
3. Executar payload didático (ex. `' OR '1'='1`, `<script>alert(1)</script>`, `;id`, `../../../etc/passwd`, JWT `none`, `role=admin`) → em `low` deve explorar; em `impossible` deve bloquear.
4. Trocar nível via UI → persiste após reload e após `restart` container.
5. View Source cada nível → código exibido corresponde ao comportamento observado.
6. Reset → dados do lab voltam ao seed, sessão mantida.

### 20.2. Testes de integração

- Fluxo completo: login → dashboard (20 cards) → lab → level switch → view source → reset → logout → acesso negado sem login.
- Cross-módulo: nível de `sqli` não afeta `xss`; guestbook de `xss_stored` aparece só lá; tokens API não vazam para web.

### 20.3. Testes de API

```bash
# login JWT
curl -s -X POST http://localhost:2300/api/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"password"}'
# IDOR low deve permitir /api/users/2 com token de user 1; impossible deve 403
curl -s http://localhost:2300/api/users/2 -H "Authorization: Bearer $JWT"
# versioning
curl -s http://localhost:2300/api/secrets -H "X-API-Version: v1"
# mass assignment
curl -s -X POST http://localhost:2300/api/users -H 'Content-Type: application/json' -d '{"name":"x","role":"admin"}'
# view source + level
curl -s http://localhost:2300/source/sqli/low | head -c 200
curl -s -X POST http://localhost:2300/level/sqli -d "level=impossible" -b cookies.txt -c cookies.txt -v
curl -s -X POST http://localhost:2300/reset -b cookies.txt -c cookies.txt -v
```

### 20.4. Testes de banco

- `sqlite3 data/duno.db ".tables"` → 7 tabelas; `.schema` confere DDL; `PRAGMA foreign_key_check;` → vazio; `PRAGMA integrity_check;` → `ok`.
- Idempotência: rodar `seed.py` 2× sem duplicar (contar `users`).
- Persistência: `docker compose restart` mantém `security_levels`; `rm data/duno.db` + `up` recria.

### 20.5. Testes de frontend

- Sem console errors (DevTools), layout 320px/768px/1280px, modal abre/fecha/ESC, Prism com e sem CDN (bloquear CDN e reabrir), forms sem JS (desabilitar JS e submeter).

### 20.6. Testes de segurança (lab-local)

- Confirmar que falhas `low` são exploráveis **e** que `impossible` bloqueia (matriz 20×4).
- Confirmar hardening global: `Set-Cookie HttpOnly`, sem traceback em 404/500, `SECRET_KEY` não default em produção lab (aviso se default), uploads `.php` bloqueados em impossible, `GET /source/../../etc/passwd` → 404 (sem LFI no loader).

### 20.7. Testes Docker

- `docker-compose up --build` do zero <60s até 200 em `/`; `logs` exibem banner+URL; `down` + `up` preserva DB; `build --no-cache` passa; `config` valida; porta 2300 responde; sem `duno.db` commitado (`git status` limpo para `*.db`).

### 20.8. Cenários de erro

- Nível inválido → 400; módulo inválido → 404; DB ausente → seed automático; DB corrompido → mensagem + instrução `rm data/duno.db`; upload >2MB → 413; JSON malformado → 400 JSON; sem login → 302 `/login`; token expirado → 401.

---

## 21. Critérios de conclusão do projeto

O projeto é considerado **concluído** quando, cumulativamente:

1. `docker-compose up --build` do zero entrega `http://localhost:2300` funcional sem intervenção manual além do comando.
2. As 20 entradas do dashboard existem, com rotas exatas do README, todas 200 autenticadas.
3. Cada módulo implementa os 4 níveis com comportamento didático distinto (low explorável, impossible bloqueia), verificado pela matriz 20×4.
4. `POST /level/<module>` persiste por (usuário, módulo) e sobrevive a restart.
5. `GET /source/<module>/<level>` retorna código fiel ao comportamento para os 80 pares (20×4).
6. `POST /reset` restaura labs preservando users/levels.
7. Login `admin/password` + logout + proteção de rotas funcionam.
8. `data/duno.db` persiste via volume; `seed.py` idempotente; `integrity_check ok`.
9. Frontend Vanilla responsivo, sem console errors, modal + level switch funcionais, Prism com fallback.
10. Nenhuma tecnologia fora da stack (sem VM, sem framework frontend, sem Postgres) salvo decisão documentada.
11. `docs/API.md` + `docs/TESTING.md` criados; README/ARCHITECTURE inalterados ou atualizados por motivo real.
12. Checklist DEVELOPMENT.md (18 itens) verde para os 20 módulos.
13. Testes §20 executados e registrados (log ou checklist assinado no PR/commit).

---

## 22. Ordem recomendada de execução

Ordem exata (sequencial salvo indicação). Não pular fases — cada uma é pré-requisito da seguinte.

```text
1.  T-001 requirements → T-002 Dockerfile → T-003 compose/env/gitignore → T-004 entrypoint
    → validar: docker build passa
2.  T-005 config/run/app mínima → validar: / responde 200 placeholder
3.  T-010 database+seed → validar: duno.db com 7 tabelas
4.  T-012 auth → validar: login/logout
5.  T-011 levels → validar: persistência
6.  T-013 source loader (com 1 módulo dummy) → validar: JSON
7.  T-014 reset → validar: limpa sem deslogar
8.  T-020 base+css+dashboard → validar: 20 cards
9.  T-021 partials+JS → validar: switch + modal
10. T-030→T-035 Fase 3 (1–6), um módulo por vez, cada um com checklist completo antes do próximo
11. T-040→T-045 Fase 4 (7–12), mesma disciplina
12. T-050→T-056 Fase 5 (13–19)
13. T-060 API Security + docs/API.md
14. T-070 seed/reset/migração final → T-071 hardening → T-072 docs finais
15. Bateria completa §20 + critérios §21
```

Paralelização permitida: após Fase 2, diferentes módulos (Fases 3–5) podem ser implementados em qualquer ordem interna, mas **um por vez com validação Docker** antes do próximo (evitairat 140 arquivos quebrados de uma vez). Nunca paralelizar `core`/`seed`/`compose` — são fundação serial.

Estimativa: ROADMAP original previa 20 dias focados para este escopo; com disciplina acima, manter como referência (F0:1d, F1:2d, F2:2d, F3–F5:9d, F6:2d, F7:2d, docs/polish:2d).

---

## 23. Regras para a Próximo DESENVOLVEDOR

1. **Não quebrar o que funciona.** Quando algo existir e passar nos testes §20, não refatorar por gosto. Mudança só com motivo registrado.
2. **Preservar a arquitetura definida.** Monolito Flask + Blueprints + `core/` 6 arquivos + `source/` 4 níveis + templates/static + SQLite + Docker único. Desvio (ex. SQLAlchemy, Postgres, React) exige justificativa explícita e atualização dos docs — padrão: não desviar.
3. **Utilizar Docker como único ambiente.** Validar tudo via `docker-compose up --build`. Não introduzir VM, não documentar execução bare-metal como oficial (fallback local apenas para debug, nunca como entrega).
4. **Não introduzir tecnologias desnecessárias.** Sem frameworks frontend, sem ORM pesado, sem brokers, sem Nginx, sem Swagger-server sem decisão. Prism CDN é o teto.
5. **Manter SQLite.** Arquivo `/app/data/duno.db`, volume `./data:/app/data`. Não migrar para outro SGBD.
6. **Manter Flask.** Versão 3.x, Python 3.11. Não portar para FastAPI/Django.
7. **Manter frontend Vanilla.** HTML/CSS/JS puros. Não adicionar jQuery/Bootstrap/React/Vue.
8. **Manter porta 2300 e rotas canônicas.** Qualquer mudança de rota/porta exige atualizar README + MODULES + testes.
9. **Fidelidade View Source.** `logic.py` nunca diverge de `source/*.py`. Se divergir, é bug crítico.
10. **Atualizar documentação quando necessário.** Mudança em Docker/Flask/SQLite/rotas/levels/source/reset/Blueprints → atualizar o `.md` correspondente + `docs/API.md`/`TESTING.md` se afetados.
11. **Testar cada etapa.** Nenhuma tarefa é "concluída" sem o teste da sua seção §14 executado em Docker. Não marcar checklist sem evidência (`curl`, log, screenshot textual).
12. **Não ignorar erros.** Traceback, 500 inesperado, `integrity_check` falho, build quebrado = parar e corrigir antes de avançar. Não mascarar com `try: pass`.
13. **Não alterar funcionalidades sem justificativa.** Comportamento didático (low vulnerável, impossible seguro) é requisito, não defeito. Não "corrigir" o low.
14. **Segredos e dados.** Nunca commitar `data/*.db`, `.env`, uploads reais. Usar apenas dados sintéticos de lab. `SECRET_KEY` via env.
15. **Usar os prompts canônicos.** Para novos módulos, usar o "Prompt para geração de módulo" de `BUILD_GUIDE.md`; para trabalho geral, o "System Prompt" do mesmo doc.
16. **Commits pequenos e verificáveis.** Um módulo ou um core por vez, com mensagem clara. Não fazer push sem `up --build` verde (quando houver repo remoto).
17. **Leitura obrigatória antes de codar.** Ler `README.md`, `ARCHITECTURE.md`, `DATABASE.md`, `MODULES.md`, `SECURITY_LEVELS.md`, `DEVELOPMENT.md`, `BUILD_GUIDE.md`, `DEPLOYMENT.md` e este `FINAL_PLAN.md` integralmente antes da primeira linha de código.
18. **Em dúvida, escolher a opção mais simples que preserva a spec.** Menos abstração, mais fidelidade aos docs.

---

*Fim do PLANO FINAL — DUNO (`FINAL_PLAN.md`). Próximo DESENVOLVEDOR: começar por T-001 na ordem §22, validando cada passo em Docker conforme §20.*
