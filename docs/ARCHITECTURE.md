# DUNO — Architecture

## 1. Modelo arquitetural

O DUNO utiliza uma arquitetura monolítica e dockerizada.

A aplicação inteira é executada dentro de um único container:

```text
Docker Host
└── duno-app
    ├── entrypoint.sh
    ├── Flask Application
    │   ├── Authentication & Session
    │   ├── Security Level Switcher
    │   ├── Reset Database
    │   ├── View Source Loader
    │   ├── Web Vulnerability Blueprints
    │   └── API Security Blueprint
    └── SQLite
        └── /app/data/duno.db
```

## 2. Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11 |
| Framework | Flask 3.x |
| Banco | SQLite |
| Frontend | HTML/CSS/JavaScript Vanilla |
| Containerização | Docker |
| Orquestração local | Docker Compose |
| Persistência | Volume `./data:/app/data` |

## 3. Regra de execução

O projeto deve ser executado através de Docker.

Fluxo:

```text
docker-compose up
        ↓
Container duno-app
        ↓
entrypoint.sh
        ↓
Inicialização do SQLite, se necessário
        ↓
Flask
        ↓
Porta 2300
```

Não existe dependência de VM na arquitetura do projeto.

## 4. Estrutura interna

### Core

```text
core/
├── __init__.py
├── database.py
├── security_levels.py
├── reset.py
├── source_loader.py
├── auth.py
└── decorators.py
```

Responsabilidades:

- conexão com o banco;
- níveis de segurança;
- reset;
- carregamento de source;
- autenticação;
- decorators compartilhados.

### Modules

Cada vulnerabilidade é organizada como Blueprint independente:

```text
modules/
└── <module>/
    ├── __init__.py
    ├── routes.py
    ├── logic.py
    └── source/
        ├── low.py
        ├── medium.py
        ├── high.py
        └── impossible.py
```

## 5. Blueprints

A aplicação utiliza Blueprints para separar os módulos sem transformar o projeto em múltiplos serviços.

Cada Blueprint contém a lógica necessária para:

- registrar as rotas;
- receber entradas;
- selecionar o nível;
- executar a lógica do laboratório;
- renderizar o template.

## 6. View Source

O fluxo é:

```text
Usuário
  ↓
View Source
  ↓
GET /source/<module>/<level>
  ↓
Source Loader
  ↓
modules/<module>/source/<level>.py
  ↓
Código retornado
  ↓
Modal no frontend
```

A especificação do projeto utiliza `importlib` e `inspect.getsource()` para carregar o código correspondente.

## 7. Security Level

O nível selecionado pelo usuário é persistido por módulo:

```text
POST /level/<module>
        ↓
SQLite
        ↓
security_levels
```

Valores aceitos:

```text
low
medium
high
impossible
```

## 8. Reset

O reset é exposto por:

```text
POST /reset
```

A lógica de reset deve restaurar os dados do laboratório e executar o seed novamente conforme as regras do projeto.

## 9. Templates

```text
templates/
├── base.html
├── index.html
├── login.html
├── _level_switch.html
├── _view_source_modal.html
└── modules/
```

## 10. Static

```text
static/
├── css/duno.css
├── js/duno.js
├── js/view_source.js
└── uploads/
```

## 11. Banco

O SQLite fica em:

```text
/app/data/duno.db
```

No host:

```text
data/duno.db
```

Persistência:

```text
./data:/app/data
```

## 12. Porta

A aplicação escuta em:

```text
2300
```

Docker Compose deve publicar:

```text
2300:2300
```
