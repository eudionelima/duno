# DUNO — Security and Responsible Use

## Natureza do projeto

O DUNO é deliberadamente vulnerável.

Seu objetivo é permitir treinamento controlado em segurança de aplicações web e APIs.

Por esse motivo, o projeto não deve ser tratado como software seguro para produção.

## Ambiente

A execução suportada é:

```text
Docker
Docker Compose
```

O laboratório deve permanecer isolado e com acesso controlado.

Não utilize VM como requisito de execução ou documentação de deploy.

## Rede

A aplicação usa:

```text
2300
```

Mantenha essa porta acessível somente no ambiente necessário para o laboratório.

Não exponha o DUNO diretamente à Internet.

## Dados

Não utilize:

- senhas reais;
- tokens reais;
- informações pessoais reais;
- dados de clientes;
- arquivos confidenciais.

Utilize somente dados criados especificamente para o laboratório.

## Credenciais de laboratório

O exemplo de configuração original utiliza:

```text
admin / password
```

Essas credenciais existem para o laboratório e não devem ser reutilizadas em sistemas reais.

## Uploads

O projeto possui:

```text
static/uploads/
```

Arquivos enviados aos módulos devem ser considerados não confiáveis.

## Reset

O recurso:

```text
POST /reset
```

pode restaurar ou apagar dados usados pelo laboratório.

Não armazene dados importantes no SQLite do DUNO.

## Uso responsável

O DUNO deve ser utilizado somente em ambientes sob controle do usuário ou em sistemas para os quais exista autorização explícita para testes.

O objetivo é treinamento, desenvolvimento de conhecimento e validação de conceitos de segurança.
