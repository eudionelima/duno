# DUNO — Designed Unsecure Network Operations

Plataforma web deliberadamente vulnerável para treinamento prático de segurança de aplicações web e APIs.

## Visão geral

O DUNO é uma aplicação web deliberadamente vulnerável, empacotada em Docker, que reúne uma interface única para laboratórios de segurança.

A arquitetura definida para o projeto utiliza:

- Python 3.11
- Flask 3.x
- SQLite
- HTML
- CSS
- JavaScript Vanilla
- Docker
- Docker Compose

A plataforma possui 19 módulos de vulnerabilidades web clássicas e um módulo especial de API Security.

Cada módulo possui quatro níveis:

```text
Low
Medium
High
Impossible
```

Também existem funcionalidades globais para:

- seleção do nível de segurança;
- visualização do código através de View Source;
- reset do banco de dados;
- dashboard central.

## Objetivo

O DUNO foi projetado como um laboratório controlado para estudar vulnerabilidades, compreender diferentes níveis de implementação e comparar vulnerabilidade com mitigação.

O projeto é intencionalmente inseguro e não deve ser utilizado como aplicação de produção.

## Ambiente de execução

O único ambiente de execução suportado pelo projeto é:

```text
Docker / Docker Compose
```

O projeto não utiliza VM como requisito de execução.

## Início rápido

Clone o repositório:

```bash
git clone <repository-url>
cd duno
```

Inicialize:

```bash
docker-compose up --build
```

A aplicação estará disponível em:

```text
http://localhost:2300
```

Para executar em segundo plano:

```bash
docker-compose up --build -d
```

Para parar:

```bash
docker-compose down
```

## Arquitetura resumida

```text
Docker Host
└── Container: duno-app
    ├── Python 3.11
    ├── Flask
    ├── SQLite
    ├── Core
    ├── Web Vulnerability Modules
    └── API Security
```

Persistência do SQLite:

```text
./data:/app/data
```

Banco:

```text
data/duno.db
```

Porta:

```text
2300
```

## Módulos

| # | Módulo | Rota |
|---:|---|---|
| 1 | Brute Force | `/brute_force` |
| 2 | Command Injection | `/command_injection` |
| 3 | CSRF | `/csrf` |
| 4 | File Inclusion | `/file_inclusion` |
| 5 | File Upload | `/file_upload` |
| 6 | Insecure CAPTCHA | `/captcha` |
| 7 | SQL Injection | `/sqli` |
| 8 | SQL Injection (Blind) | `/sqli_blind` |
| 9 | Weak Session IDs | `/weak_session` |
| 10 | XSS (DOM) | `/xss_dom` |
| 11 | XSS (Reflected) | `/xss_reflected` |
| 12 | XSS (Stored) | `/xss_stored` |
| 13 | CSP Bypass | `/csp_bypass` |
| 14 | JavaScript Attacks | `/js_attacks` |
| 15 | Authorisation Bypass | `/auth_bypass` |
| 16 | Open HTTP Redirect | `/open_redirect` |
| 17 | Cryptography | `/crypto` |
| 18 | API Versioning | `/api_versioning` |
| 19 | Mass Assignment | `/mass_assignment` |
| 20 | API Security | `/api/*` |

## Níveis de segurança

Cada laboratório implementa:

```text
Low
Medium
High
Impossible
```

A progressão representa, de forma didática:

```text
Implementação vulnerável
        ↓
Mitigação básica
        ↓
Mitigação mais forte, porém incompleta
        ↓
Implementação segura
```

## Recursos globais

### View Source

Endpoint:

```text
GET /source/<module>/<level>
```

Permite visualizar o código correspondente ao módulo e ao nível selecionado.

### Security Level

Endpoint:

```text
POST /level/<module>
```

Persiste o nível selecionado no SQLite.

### Reset Database

Endpoint:

```text
POST /reset
```

Restaura os dados do laboratório conforme a estratégia definida pelo projeto.

## Estrutura do repositório

```text
duno/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── run.py
├── config.py
├── seed.py
├── data/
├── core/
├── modules/
├── templates/
├── static/
└── docs/
```

## Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Deploy](docs/DEPLOYMENT.md)
- [Desenvolvimento](docs/DEVELOPMENT.md)
- [Módulos](docs/MODULES.md)
- [Níveis de Segurança](docs/SECURITY_LEVELS.md)
- [Banco de Dados](docs/DATABASE.md)
- [Guia para IA](docs/AI_BUILD_GUIDE.md)
- [Roadmap](docs/ROADMAP.md)
- [Segurança e Uso Responsável](docs/SECURITY.md)

## Aviso de segurança

O DUNO é deliberadamente vulnerável.

Execute a plataforma somente através do ambiente Docker definido pelo projeto e mantenha a porta da aplicação restrita ao ambiente de laboratório.

Não utilize dados reais dentro do laboratório.

## Status

Projeto em desenvolvimento.
