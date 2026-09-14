# DUNO — Security Levels

O DUNO utiliza quatro níveis de segurança para cada laboratório:

```text
Low
Medium
High
Impossible
```

## Low

Implementação deliberadamente vulnerável.

Características esperadas:

- ausência de controles adequados;
- validação insuficiente;
- implementação insegura.

O objetivo é facilitar a identificação do problema durante o treinamento.

## Medium

Implementação com uma mitigação básica.

Exemplos previstos pela especificação:

- escaping simples;
- blacklist;
- controles parciais.

O objetivo é demonstrar que uma mitigação superficial pode não ser suficiente.

## High

Implementação mais resistente, mas ainda com uma falha lógica ou de desenho.

A especificação original usa como exemplo conceitual:

- prepared statements com um problema relacionado à sessão.

## Impossible

Implementação considerada segura para o cenário do laboratório.

A especificação original cita como exemplos:

- prepared statements;
- rate limit;
- audit log;
- controles completos.

## Persistência

O nível é armazenado por usuário e módulo na tabela:

```text
security_levels
```

Campos:

```text
user_id
module
level
```

Valores permitidos:

```text
low
medium
high
impossible
```

## Endpoint

```text
POST /level/<module>
```

Parâmetro:

```text
level=low|medium|high|impossible
```

## View Source

O código correspondente ao nível pode ser obtido por:

```text
GET /source/<module>/<level>
```

Exemplo:

```text
/source/sqli/low
/source/sqli/medium
/source/sqli/high
/source/sqli/impossible
```

## Finalidade didática

A funcionalidade permite comparar diretamente:

```text
Código vulnerável
      ↓
Mitigação básica
      ↓
Mitigação incompleta
      ↓
Código seguro
```
