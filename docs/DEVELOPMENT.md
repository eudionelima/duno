# DUNO — Development Guide

## Stack

```text
Python 3.11
Flask 3.x
SQLite
HTML
CSS
JavaScript Vanilla
Docker
Docker Compose
```

## Regra principal

O projeto mantém uma arquitetura monolítica e deve continuar sendo executado através de Docker.

Alterações no ambiente de execução devem preservar essa regra.

## Estrutura de um módulo

```text
modules/example/
├── __init__.py
├── routes.py
├── logic.py
└── source/
    ├── low.py
    ├── medium.py
    ├── high.py
    └── impossible.py
```

Template:

```text
templates/modules/example.html
```

## Responsabilidade dos arquivos

### `__init__.py`

Cria e/ou exporta o Blueprint.

### `routes.py`

Define as rotas HTTP e a integração com os templates.

### `logic.py`

Implementa a seleção e execução da lógica correspondente ao nível.

### `source/`

Contém os arquivos usados pelo mecanismo de View Source.

## Rotas esperadas

Exemplo:

```text
GET  /example
POST /example
GET  /source/example/<level>
POST /level/example
```

## Regras para novos módulos

Todo módulo deve:

- usar Blueprint;
- possuir quatro níveis;
- possuir quatro arquivos em `source/`;
- possuir template próprio;
- aparecer no dashboard;
- funcionar com View Source;
- funcionar com Security Level;
- respeitar o reset do laboratório.

## Frontend

O frontend utiliza apenas:

```text
HTML
CSS
JavaScript Vanilla
```

Não adicionar frameworks frontend sem uma decisão arquitetural explícita.

Arquivos principais:

```text
static/css/duno.css
static/js/duno.js
static/js/view_source.js
```

## Prism.js

A especificação original permite utilizar Prism.js via CDN para syntax highlighting do View Source.

## Desenvolvimento com Docker

O fluxo recomendado de validação é:

```bash
docker-compose up --build
```

Depois de alterar o código:

```bash
docker-compose up --build
```

Para visualizar logs:

```bash
docker-compose logs -f
```

## Checklist

Antes de considerar um módulo concluído:

- [ ] Blueprint registrado.
- [ ] Rota principal criada.
- [ ] `logic.py` criado.
- [ ] Low implementado.
- [ ] Medium implementado.
- [ ] High implementado.
- [ ] Impossible implementado.
- [ ] `source/low.py` criado.
- [ ] `source/medium.py` criado.
- [ ] `source/high.py` criado.
- [ ] `source/impossible.py` criado.
- [ ] Template criado.
- [ ] Dashboard atualizado.
- [ ] View Source testado.
- [ ] Security Level testado.
- [ ] Reset testado.
- [ ] Deploy Docker validado.

## Compatibilidade

Alterações devem preservar:

- Python 3.11;
- Flask 3.x;
- SQLite;
- Docker;
- Docker Compose;
- porta 2300;
- estrutura dos Blueprints.
