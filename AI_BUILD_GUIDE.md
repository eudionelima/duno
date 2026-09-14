# DUNO — Build Guide

Este documento estabelece as diretrizes para desenvolvedores que criam, modificam ou contribuem com o código da DUNO, uma plataforma deliberadamente vulnerável desenvolvida para profissionais de cibersegurança e estudantes. Seu objetivo é proporcionar um ambiente seguro e controlado para estudar e praticar, na prática, conceitos de segurança de aplicações e compreender como vulnerabilidades podem ocorrer em cenários próximos aos encontrados no mundo real.

## Identidade do projeto

Nome oficial:

```text
DUNO — Designed Unsecure Network Operations
```

Não utilizar nomes anteriores do projeto na documentação ou no código novo.

## Stack obrigatória

```text
Python 3.11
Flask 3.x
SQLite
HTML/CSS/JavaScript Vanilla
Docker
Docker Compose
```

## Regra de execução

O projeto deve ser executado através de Docker.

Não adicionar VM como requisito, etapa de deploy ou arquitetura alternativa.

## System Prompt

```text
You are an expert Python/Flask developer working on DUNO — DUNO — Designed Unsecure Network Operations.

DUNO is a deliberately insecure educational web application used for controlled security training.

Required stack:
- Python 3.11
- Flask 3.x
- SQLite
- HTML/CSS/JavaScript Vanilla
- Docker
- Docker Compose

Architecture:
- Single Flask application
- Flask Blueprints for vulnerability modules
- SQLite database at data/duno.db
- Application port 2300
- Four security levels: low, medium, high, impossible
- View Source feature
- Reset Database feature

Important:
- Docker is the only supported execution environment.
- Do not introduce VM-based deployment.
- Do not introduce frontend frameworks unless explicitly requested.
- Preserve the existing DUNO directory structure.
- Keep the code compatible with Python 3.11.
- Keep all modules integrated into the same Flask application.
```

## Regras dos módulos

Cada módulo deve possuir:

```text
modules/<module>/
├── __init__.py
├── routes.py
├── logic.py
└── source/
    ├── low.py
    ├── medium.py
    ├── high.py
    └── impossible.py
```

Também deve possuir:

```text
templates/modules/<module>.html
```

## View Source

O mecanismo deve continuar compatível com:

```text
GET /source/<module>/<level>
```

A implementação documentada utiliza:

```text
importlib
inspect.getsource()
```

## Security Levels

Cada módulo deve implementar:

```text
low()
medium()
high()
impossible()
```

A progressão deve permanecer didática:

```text
vulnerável
    ↓
mitigação básica
    ↓
mitigação incompleta
    ↓
seguro
```

## Core

Os componentes centrais previstos são:

```text
core/database.py
core/security_levels.py
core/reset.py
core/source_loader.py
core/auth.py
core/decorators.py
```

## Prompt para geração de módulo

```text
Create the <MODULE> module for DUNO — DUNO — Designed Unsecure Network Operations.

Generate:

modules/<module>/__init__.py
modules/<module>/routes.py
modules/<module>/logic.py
modules/<module>/source/low.py
modules/<module>/source/medium.py
modules/<module>/source/high.py
modules/<module>/source/impossible.py
templates/modules/<module>.html

Requirements:
- Use Flask Blueprint.
- Implement four security levels.
- Preserve the existing DUNO architecture.
- Integrate with Security Level persistence.
- Integrate with View Source.
- Keep the module compatible with Docker.
- Do not add new frameworks.
- Do not alter global architecture without explicit instruction.
```

## Mudanças arquiteturais

Sempre que uma alteração afetar:

- Docker;
- Flask;
- SQLite;
- rotas globais;
- Security Levels;
- View Source;
- Reset;
- Blueprints;

a documentação correspondente deve ser atualizada.

## Política de arquivos

Ao gerar código:

- informe o caminho de cada arquivo;
- não omita arquivos estruturais;
- mantenha nomes consistentes;
- preserve compatibilidade com o restante da plataforma;
- não renomeie o projeto;
- utilize somente `DUNO — DUNO — Designed Unsecure Network Operations`.
