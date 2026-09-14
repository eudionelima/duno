# DUNO — Deployment

## Requisito

O DUNO deve ser executado exclusivamente através de Docker e Docker Compose.

## Pré-requisitos

Instale:

- Docker;
- Docker Compose.

Não é necessário configurar uma VM para executar o projeto.

## Deploy

Na raiz do projeto:

```bash
docker-compose up --build
```

Durante a inicialização:

```text
Build da imagem
    ↓
Criação do container
    ↓
Execução do entrypoint.sh
    ↓
Inicialização do banco, se necessário
    ↓
Inicialização do Flask
```

## Execução em background

```bash
docker-compose up --build -d
```

## Parar

```bash
docker-compose down
```

## Rebuild completo

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Porta

A aplicação utiliza:

```text
2300
```

Acesse:

```text
http://localhost:2300
```

## Persistência

O projeto utiliza:

```yaml
volumes:
  - ./data:/app/data
```

O arquivo persistido é:

```text
data/duno.db
```

## Entrypoint

O `entrypoint.sh` possui três responsabilidades:

1. exibir o banner do DUNO;
2. verificar e inicializar o banco;
3. executar o Flask.

## Inicialização do banco

Quando o arquivo não existe:

```text
/app/data/duno.db
```

o entrypoint executa:

```bash
python seed.py
```

## Verificação

Depois do deploy:

```text
http://localhost:2300
```

O terminal deve informar:

- URL;
- módulos;
- níveis;
- funcionalidades;
- tecnologia utilizada.

## Troubleshooting

### Porta 2300 ocupada

Verifique os containers e processos que estejam utilizando a porta.

### Mudança no código não aparece

Reconstrua:

```bash
docker-compose up --build
```

### Banco precisa ser recriado

Use o mecanismo de reset da própria plataforma ou recrie o ambiente Docker conforme a necessidade do laboratório.

### Container não inicia

Verifique:

```bash
docker-compose logs
```

e confirme:

- Docker em execução;
- `requirements.txt`;
- `entrypoint.sh`;
- porta `2300`;
- permissões necessárias;
- diretório `data`.

## Regra de isolamento

O DUNO deve permanecer acessível somente no ambiente onde foi implantado.

Não publique a porta `2300` diretamente na Internet.
