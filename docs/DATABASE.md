# DUNO — Database

## Banco

O DUNO utiliza SQLite como banco central.

No host:

```text
data/duno.db
```

No container:

```text
/app/data/duno.db
```

## Persistência

Docker Compose utiliza:

```text
./data:/app/data
```

## Tabelas

### users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

O campo `role` representa os papéis:

```text
user
admin
```

### security_levels

```sql
CREATE TABLE security_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    module TEXT NOT NULL,
    level TEXT NOT NULL CHECK(level IN ('low','medium','high','impossible')),
    UNIQUE(user_id, module),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### guestbook

Usada em cenários relacionados a XSS Stored:

```sql
CREATE TABLE guestbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### secrets

Usada em cenários relacionados a Cryptography e JavaScript Attacks:

```sql
CREATE TABLE secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT,
    value TEXT
);
```

### api_tokens

Usada pelo módulo de API Security:

```sql
CREATE TABLE api_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token TEXT,
    version TEXT
);
```

### captcha_challenges

Usada pelo módulo de CAPTCHA:

```sql
CREATE TABLE captcha_challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge TEXT,
    answer TEXT,
    used INTEGER DEFAULT 0
);
```

### audit_log

Usada nos cenários que necessitam de registros de auditoria:

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    ip TEXT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Seed

O banco inicial é criado por:

```bash
python seed.py
```

O `entrypoint.sh` executa o seed quando:

```text
/app/data/duno.db
```

não existe.

## Reset

A aplicação fornece:

```text
POST /reset
```

O reset deve restaurar os dados do laboratório e executar novamente o seed conforme a estratégia definida pela aplicação.
