#!/usr/bin/env python3
"""generate_templates.py — gera todos os templates de módulo."""
import os

BASE = "/home/dione/Projects/duno"
TMPL = os.path.join(BASE, "templates", "modules")

def write(slug, content):
    path = os.path.join(TMPL, f"{slug}.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"[write] templates/modules/{slug}.html")


def base_template(slug, num, title, icon, desc, lab_content, info_content):
    return f'''{{% extends "base.html" %}}
{{% block title %}}{title}{{% endblock %}}

{{% block content %}}
<div class="module-page">
  <div class="breadcrumb">
    <a href="{{{{ url_for('index') }}}}">Dashboard</a>
    <span class="breadcrumb-sep">›</span>
    <span>#{num} {title}</span>
  </div>

  <div class="module-header">
    <div class="module-title-row">
      <h1 class="module-title">{icon} {title}</h1>
      <p class="module-desc">{desc}</p>
    </div>
    <div class="module-controls">
      {{% set current_level = level %}}
      {{% include '_level_switch.html' with context %}}
      <button class="btn btn-ghost btn-sm" onclick="openSourceModal('{slug}', '{{{{ level }}}}')">
        &lt;/&gt; View Source
      </button>
    </div>
  </div>

  <div class="module-body">
    <div class="panel">
      <div class="panel-title">Laboratório — <span class="level-badge level-{{{{ level }}}}">{{{{ level }}}}</span></div>
{lab_content}
    </div>

    <div class="panel">
      <div class="panel-title">Como funciona</div>
{info_content}
    </div>
  </div>
</div>
{{% endblock %}}
'''


# ── Templates individuais ──────────────────────────────────────────────────────

# command_injection
write("command_injection", base_template(
    "command_injection", "2", "Command Injection", "💻",
    "Injeção de comandos via entrada controlada",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Execute comandos arbitrários. Tente <code>127.0.0.1; id</code> ou <code>127.0.0.1 | cat /etc/passwd</code>
      </p>
      <form method="POST" action="/command_injection" id="cmd-form">
        <div class="form-group">
          <label for="cmd-input">Comando / Host</label>
          <input type="text" id="cmd-input" name="cmd" class="form-control" placeholder="127.0.0.1" value="{{ cmd }}" />
        </div>
        <button type="submit" class="btn btn-primary">Executar</button>
      </form>
      {% if result is not none %}
      <div class="result-box raw" style="margin-top:1rem"><pre>{{ result }}</pre></div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Sem sanitização — <code>shell=True</code> com input direto. Injete com <code>; id</code>{% endif %}
        {% if level == 'medium' %}Blacklist de <code>; && || ` $ |</code> — bypassável com <code>%0a</code> ou outros separadores{% endif %}
        {% if level == 'high' %}Regex <code>^[\\w.\\- ]+$</code> — previne a maioria mas subshells via <code>$(...)</code> podem funcionar{% endif %}
        {% if level == 'impossible' %}Whitelist de comandos + <code>shlex.split</code> sem <code>shell=True</code> — injeção impossível{% endif %}
      </div>''',
))

# csrf
write("csrf", base_template(
    "csrf", "3", "CSRF", "🎭",
    "Cross-Site Request Forgery — requisição forjada entre sites",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Altere o nome de usuário sem o conhecimento da vítima. Forje uma requisição POST para <code>/csrf</code>.
      </p>
      <form method="POST" action="/csrf" id="csrf-form">
        <div class="form-group">
          <label for="new-email">Novo username</label>
          <input type="text" id="new-email" name="new_email" class="form-control" placeholder="novo_nome" />
        </div>
        {% if level in ('high', 'impossible') %}
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}" />
        {% endif %}
        <button type="submit" class="btn btn-primary">Alterar</button>
      </form>
      {% if result %}
      <div class="result-box {% if 'inválido' in result or 'ausente' in result %}error{% else %}success{% endif %}">{{ result }}</div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Sem token CSRF — qualquer site pode POST para <code>/csrf</code> com o cookie da vítima{% endif %}
        {% if level == 'medium' %}Verifica Referer — bypassável: Referer ausente ou com <code>localhost</code> na URL de origem{% endif %}
        {% if level == 'high' %}Token CSRF fixo por sessão — automatização ainda possível com extração do token{% endif %}
        {% if level == 'impossible' %}Token one-time gerado por form — reuso impossível{% endif %}
      </div>''',
))

# file_inclusion
write("file_inclusion", base_template(
    "file_inclusion", "4", "File Inclusion", "📂",
    "Leitura de arquivos via parâmetro — Local File Inclusion",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Leia <code>/etc/passwd</code>. Tente <code>?page=../../../etc/passwd</code>
      </p>
      <form method="GET" action="/file_inclusion" id="fi-form">
        <div class="form-group">
          <label for="page-input">Arquivo</label>
          <input type="text" id="page-input" name="page" class="form-control"
                 placeholder="about.txt" value="{{ page }}" />
        </div>
        <button type="submit" class="btn btn-primary">Carregar</button>
      </form>
      {% if result is not none %}
      <div class="result-box raw" style="margin-top:1rem"><pre>{{ result }}</pre></div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Path concatenado diretamente — <code>../../../etc/passwd</code> funciona{% endif %}
        {% if level == 'medium' %}Bloqueia <code>../</code> — bypassável com URL encoding <code>%2e%2e/</code>{% endif %}
        {% if level == 'high' %}Whitelist de nomes — symlinks podem contornar{% endif %}
        {% if level == 'impossible' %}Whitelist + <code>os.path.realpath</code> — path traversal impossível{% endif %}
      </div>
      <div style="margin-top:0.75rem;font-size:0.82rem;color:var(--text-muted)">Arquivos disponíveis: <code>about.txt</code>, <code>help.txt</code>, <code>info.txt</code></div>''',
))

# file_upload
write("file_upload", base_template(
    "file_upload", "5", "File Upload", "📤",
    "Upload inseguro — envie arquivos arbitrários ao servidor",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Faça upload de um arquivo <code>.php</code> ou webshell. Em low, qualquer arquivo é aceito.
      </p>
      <form method="POST" action="/file_upload" enctype="multipart/form-data" id="upload-form">
        <div class="form-group">
          <label for="file-input">Arquivo</label>
          <input type="file" id="file-input" name="file" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary">Enviar</button>
      </form>
      {% if result %}
      <div class="result-box {% if 'salvo' in result or 'segurança' in result %}success{% else %}error{% endif %}">{{ result }}</div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Qualquer arquivo aceito — envie <code>shell.php</code>{% endif %}
        {% if level == 'medium' %}Valida <code>Content-Type</code> — altere via Burp para <code>image/jpeg</code>{% endif %}
        {% if level == 'high' %}Valida extensão + Content-Type — bypassável com <code>shell.php.jpg</code>{% endif %}
        {% if level == 'impossible' %}PIL valida magic bytes + recomprime + UUID — webshell impossível{% endif %}
      </div>''',
))

# captcha
write("captcha", base_template(
    "captcha", "6", "Insecure CAPTCHA", "🤖",
    "Bypass de mecanismo de CAPTCHA",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Resolva (ou bypass) o CAPTCHA. Em low, qualquer resposta é aceita pelo servidor.
      </p>
      <form method="POST" action="/captcha" id="captcha-form">
        <div class="form-group">
          <label>Desafio</label>
          <p style="color:var(--text-primary);font-weight:600;font-size:1rem">{{ challenge.question }}</p>
          <input type="hidden" name="challenge_id" value="{{ challenge.id }}" />
        </div>
        <div class="form-group">
          <label for="captcha-answer">Resposta</label>
          <input type="text" id="captcha-answer" name="answer" class="form-control" placeholder="Ex: 7" />
        </div>
        <button type="submit" class="btn btn-primary">Verificar</button>
      </form>
      {% if result %}
      <div class="result-box {% if 'correto' in result %}success{% else %}error{% endif %}">{{ result }}</div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Validação apenas no cliente (JS) — servidor aceita qualquer resposta{% endif %}
        {% if level == 'medium' %}Valida server-side mas não marca como usado — desafio reutilizável{% endif %}
        {% if level == 'high' %}Marca como usado mas desafio é texto simples — predizível{% endif %}
        {% if level == 'impossible' %}Desafio one-time com hash server-side — não é possível reutilizar ou pré-computar{% endif %}
      </div>''',
))

# sqli
write("sqli", f'''{{% extends "base.html" %}}
{{% block title %}}SQL Injection{{% endblock %}}

{{% block content %}}
<div class="module-page">
  <div class="breadcrumb">
    <a href="{{{{ url_for('index') }}}}">Dashboard</a>
    <span class="breadcrumb-sep">›</span>
    <span>#7 SQL Injection</span>
  </div>

  <div class="module-header">
    <div class="module-title-row">
      <h1 class="module-title">🗄️ SQL Injection</h1>
      <p class="module-desc">Manipulação de consultas SQL via entrada controlada</p>
    </div>
    <div class="module-controls">
      {{% set current_level = level %}}
      {{% include '_level_switch.html' with context %}}
      <button class="btn btn-ghost btn-sm" onclick="openSourceModal('sqli', '{{{{ level }}}}')">
        &lt;/&gt; View Source
      </button>
    </div>
  </div>

  <div class="module-body">
    <div class="panel">
      <div class="panel-title">Laboratório — <span class="level-badge level-{{{{ level }}}}">{{{{ level }}}}</span></div>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Extraia todos os usuários. Tente <code>1 OR 1=1--</code> ou <code>1 UNION SELECT 1,username,password_hash FROM users--</code>
      </p>
      <form method="POST" action="/sqli" id="sqli-form">
        <div class="form-group">
          <label for="user-id">User ID</label>
          <input type="text" id="user-id" name="user_id" class="form-control" placeholder="1" />
        </div>
        <button type="submit" class="btn btn-primary">Buscar</button>
      </form>
      {{% if rows %}}
      <div style="margin-top:1rem;overflow-x:auto">
        <table class="data-table">
          <thead><tr><th>ID</th><th>Username</th><th>Role</th><th>Extra</th></tr></thead>
          <tbody>
            {{% for row in rows %}}
            <tr>
              <td>{{{{ row.get('id','') }}}}</td>
              <td>{{{{ row.get('username', row.get('error','')) }}}}</td>
              <td>{{{{ row.get('role','') }}}}</td>
              <td>{{{{ row.get('password_hash', row.get('error',''))[:40] if row.get('password_hash') else '' }}}}</td>
            </tr>
            {{% endfor %}}
          </tbody>
        </table>
      </div>
      {{% endif %}}
    </div>

    <div class="panel">
      <div class="panel-title">Como funciona</div>
      <div class="alert alert-{{% if level == 'impossible' %}}success{{% elif level == 'high' %}}warning{{% else %}}error{{% endif %}}">
        {{% if level == 'low' %}}Concatenação direta: <code>WHERE id = {{input}}</code> — UNION, OR 1=1, comentários todos funcionam{{% endif %}}
        {{% if level == 'medium' %}}Blacklist de palavras — bypassável com <code>UNION/**/SELECT</code> ou variação de case{{% endif %}}
        {{% if level == 'high' %}}Prepared statement + cast para int — SQLi impossível, mas apenas IDs inteiros funcionam{{% endif %}}
        {{% if level == 'impossible' %}}Prepared statement + validação estrita de tipo positivo — completamente seguro{{% endif %}}
      </div>
    </div>
  </div>
</div>
{{% endblock %}}
''')

# sqli_blind
write("sqli_blind", base_template(
    "sqli_blind", "8", "SQL Injection (Blind)", "👁️",
    "Boolean-based e time-based blind SQL Injection",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Infira dados via respostas binárias. Tente <code>1 AND 1=1</code> vs <code>1 AND 1=2</code>.
        Em high, use time-based com <code>1 AND (SELECT COUNT(*) FROM sqlite_master)>0</code>.
      </p>
      <form method="POST" action="/sqli_blind" id="blind-form">
        <div class="form-group">
          <label for="blind-id">User ID</label>
          <input type="text" id="blind-id" name="user_id" class="form-control" placeholder="1" />
        </div>
        <button type="submit" class="btn btn-primary">Verificar</button>
      </form>
      {% if result %}
      <div class="result-box {% if 'existe' in result %}success{% else %}error{% endif %}">{{ result }}</div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Boolean-based — diferença entre true/false permite enumeração{% endif %}
        {% if level == 'medium' %}Remove aspas — injeção numérica ainda funciona{% endif %}
        {% if level == 'high' %}Vulnerável a time-based — inferência por tempo de resposta{% endif %}
        {% if level == 'impossible' %}Prepared statement — injeção impossível{% endif %}
      </div>''',
))

# weak_session
write("weak_session", base_template(
    "weak_session", "9", "Weak Session IDs", "🪪",
    "Geração de IDs de sessão previsíveis ou manipuláveis",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Preveja o próximo ID de sessão. Em low, é um contador simples.
      </p>
      <div style="margin:1rem 0">
        <p style="color:var(--text-muted);font-size:0.82rem">ID gerado para esta requisição:</p>
        <div class="result-box info" style="margin-top:0.5rem;font-family:monospace;font-size:0.95rem">
          {{ new_sid }}
        </div>
      </div>
      <form method="GET" action="/weak_session" id="sid-form">
        <button type="submit" class="btn btn-primary">Gerar novo ID</button>
      </form>''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Sequencial — ID = 1, 2, 3… trivialmente previsível{% endif %}
        {% if level == 'medium' %}MD5(timestamp) — previsível se o atacante souber a hora{% endif %}
        {% if level == 'high' %}SHA1(timestamp + random) — entropia baixa com random não-criptográfico{% endif %}
        {% if level == 'impossible' %}<code>secrets.token_hex(32)</code> — 256 bits de entropia criptográfica{% endif %}
      </div>''',
))

# xss_dom
write("xss_dom", base_template(
    "xss_dom", "10", "XSS (DOM)", "🌐",
    "Cross-Site Scripting via manipulação do DOM",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Execute JavaScript injetando no parâmetro name. Tente <code>&lt;img src=x onerror=alert(1)&gt;</code>
      </p>
      <form method="POST" action="/xss_dom" id="dom-form">
        <div class="form-group">
          <label for="dom-name">Nome</label>
          <input type="text" id="dom-name" name="name" class="form-control" placeholder="<img src=x onerror=alert(1)>" />
        </div>
        <button type="submit" class="btn btn-primary">Enviar</button>
      </form>
      {% if result is not none %}
      <div style="margin-top:1rem">
        <p style="font-size:0.8rem;color:var(--text-muted)">Output (DOM):</p>
        {% if level == 'impossible' %}
        <div class="result-box">Olá, {{ result }}!</div>
        {% else %}
        <div id="dom-output" class="result-box"></div>
        <script>
          document.getElementById('dom-output').innerHTML = {{ result | tojson }};
        </script>
        {% endif %}
      </div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}innerHTML sem sanitização — qualquer HTML/JS é executado{% endif %}
        {% if level == 'medium' %}Remove &lt;script&gt; — bypassável com &lt;img onerror=...&gt;{% endif %}
        {% if level == 'high' %}Regex mais abrangente — bypassável com SVG ou outros vetores{% endif %}
        {% if level == 'impossible' %}textContent em vez de innerHTML — XSS via DOM impossível{% endif %}
      </div>''',
))

# xss_reflected
write("xss_reflected", base_template(
    "xss_reflected", "11", "XSS (Reflected)", "↩️",
    "XSS refletido via parâmetros HTTP",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Injete e execute JavaScript. Tente <code>&lt;script&gt;alert(1)&lt;/script&gt;</code>
      </p>
      <form method="POST" action="/xss_reflected" id="xss-r-form">
        <div class="form-group">
          <label for="xss-name">Nome</label>
          <input type="text" id="xss-name" name="name" class="form-control"
                 placeholder="<script>alert(1)</script>" />
        </div>
        <button type="submit" class="btn btn-primary">Enviar</button>
      </form>
      {% if result is not none %}
      <div class="result-box" style="margin-top:1rem">
        {% if level == 'impossible' %}
        Olá, {{ result }}!
        {% else %}
        {{ result }}
        {% endif %}
      </div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Markup() sem escape — <code>&lt;script&gt;</code> executado diretamente{% endif %}
        {% if level == 'medium' %}Remove &lt;script&gt; case-insensitive — bypassável com &lt;ScRiPt&gt; ou eventos{% endif %}
        {% if level == 'high' %}escape() + Markup() — combinação segura mas depende do uso correto{% endif %}
        {% if level == 'impossible' %}escape() puro + Jinja2 autoescaping — injeção impossível{% endif %}
      </div>''',
))

# xss_stored
write("xss_stored", f'''{{% extends "base.html" %}}
{{% block title %}}XSS (Stored){{% endblock %}}

{{% block content %}}
<div class="module-page">
  <div class="breadcrumb">
    <a href="{{{{ url_for('index') }}}}">Dashboard</a>
    <span class="breadcrumb-sep">›</span>
    <span>#12 XSS (Stored)</span>
  </div>

  <div class="module-header">
    <div class="module-title-row">
      <h1 class="module-title">💾 XSS (Stored)</h1>
      <p class="module-desc">XSS persistido no guestbook</p>
    </div>
    <div class="module-controls">
      {{% set current_level = level %}}
      {{% include '_level_switch.html' with context %}}
      <button class="btn btn-ghost btn-sm" onclick="openSourceModal('xss_stored', '{{{{ level }}}}')">
        &lt;/&gt; View Source
      </button>
    </div>
  </div>

  <div class="module-body">
    <div class="panel">
      <div class="panel-title">Guestbook — <span class="level-badge level-{{{{ level }}}}">{{{{ level }}}}</span></div>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Injete XSS que persiste para todos os visitantes. Tente <code>&lt;script&gt;alert(document.cookie)&lt;/script&gt;</code>
      </p>
      <form method="POST" action="/xss_stored" id="guestbook-form">
        <div class="form-group">
          <label for="gb-name">Nome</label>
          <input type="text" id="gb-name" name="name" class="form-control" placeholder="Seu nome" />
        </div>
        <div class="form-group">
          <label for="gb-msg">Mensagem</label>
          <textarea id="gb-msg" name="message" class="form-control" rows="3" placeholder="Sua mensagem..."></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Postar</button>
      </form>

      <div style="margin-top:1.5rem">
        <p style="font-size:0.8rem;color:var(--text-muted);margin-bottom:0.75rem">Entradas do guestbook:</p>
        {{% if entries %}}
        <table class="data-table">
          <thead><tr><th>#</th><th>Nome</th><th>Mensagem</th></tr></thead>
          <tbody>
            {{% for entry in entries %}}
            <tr>
              <td>{{{{ entry.id }}}}</td>
              <td>{{{{ entry.name }}}}</td>
              <td>{{{{ entry.message }}}}</td>
            </tr>
            {{% endfor %}}
          </tbody>
        </table>
        {{% else %}}
        <p style="color:var(--text-muted);font-size:0.85rem">Sem entradas ainda.</p>
        {{% endif %}}
      </div>
    </div>

    <div class="panel">
      <div class="panel-title">Como funciona</div>
      <div class="alert alert-{{% if level == 'impossible' %}}success{{% elif level == 'high' %}}warning{{% else %}}error{{% endif %}}">
        {{% if level == 'low' %}}Salva raw + renderiza com Markup() — XSS executado para todos os visitantes{{% endif %}}
        {{% if level == 'medium' %}}Remove &lt;script&gt; mas renderiza raw — bypassável com eventos HTML5{{% endif %}}
        {{% if level == 'high' %}}Escapa na gravação mas renderiza com Markup() — escape revertido na saída{{% endif %}}
        {{% if level == 'impossible' %}}Salva raw + Jinja2 autoescaping na saída — injeção impossível{{% endif %}}
      </div>
    </div>
  </div>
</div>
{{% endblock %}}
''')

# csp_bypass
write("csp_bypass", base_template(
    "csp_bypass", "13", "CSP Bypass", "🛡️",
    "Bypass de Content Security Policy",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Execute JavaScript apesar do CSP. Em medium, use inline handlers. Em high, explore JSONP no CDN.
      </p>
      <form method="POST" action="/csp_bypass" id="csp-form">
        <div class="form-group">
          <label for="csp-name">Payload</label>
          <input type="text" id="csp-name" name="name" class="form-control"
                 placeholder="<img src=x onerror=alert(1)>" />
        </div>
        <button type="submit" class="btn btn-primary">Testar</button>
      </form>
      {% if result is not none %}
      <div class="result-box" style="margin-top:1rem">
        {% if level == 'impossible' %}
        {{ result }}
        {% else %}
        {{ result | safe }}
        {% endif %}
      </div>
      {% endif %}
      <div style="margin-top:1rem;font-size:0.8rem;color:var(--text-muted)">
        CSP atual: <code>{{ csp_header or "nenhum" }}</code>
      </div>''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Sem CSP — scripts externos e inline livres{% endif %}
        {% if level == 'medium' %}CSP com 'unsafe-inline' — XSS inline ainda possível{% endif %}
        {% if level == 'high' %}CSP com CDN sem hash/nonce — JSONP endpoint no CDN pode ser explorado{% endif %}
        {% if level == 'impossible' %}CSP com nonce por requisição sem unsafe-inline — execução de JS não autorizada impossível{% endif %}
      </div>''',
))

# js_attacks
write("js_attacks", base_template(
    "js_attacks", "14", "JavaScript Attacks", "⚡",
    "Manipulação de valores client-side",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Compre o produto por R$ 0,01 manipulando o campo de preço. Em low, altere via DevTools.
      </p>
      <form method="POST" action="/js_attacks" id="js-form">
        <div class="form-group">
          <label for="product">Produto</label>
          <select id="product" name="product_id" class="form-control">
            <option value="1">Produto A — R$ 99,90</option>
            <option value="2">Produto B — R$ 199,90</option>
            <option value="3">Produto C — R$ 49,90</option>
          </select>
        </div>
        {% if level != 'impossible' %}
        <div class="form-group">
          <label for="price">Preço (client-side)</label>
          <input type="number" id="price" name="price" class="form-control"
                 placeholder="99.90" step="0.01" min="0" />
        </div>
        {% endif %}
        <button type="submit" class="btn btn-primary">Comprar</button>
      </form>
      {% if result %}
      <div class="result-box {% if 'realizada' in result %}success{% else %}error{% endif %}">{{ result }}</div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Preço enviado pelo cliente sem validação — altere para 0.01 no formulário{% endif %}
        {% if level == 'medium' %}Valida server-side mas aceita float — experimente valores edge case{% endif %}
        {% if level == 'high' %}Consulta banco por product_id — mas product_id é manipulável{% endif %}
        {% if level == 'impossible' %}Preço definido exclusivamente no servidor — cliente não controla valor{% endif %}
      </div>''',
))

# auth_bypass
write("auth_bypass", base_template(
    "auth_bypass", "15", "Authorisation Bypass", "🚪",
    "Acesso indevido a área administrativa",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Acesse a área admin sem ter permissão. Em medium, forje o cookie <code>admin=1</code> via DevTools.
      </p>
      <div class="result-box {% if access %}success{% else %}error{% endif %}" style="margin:1rem 0">
        {% if access %}
        ✅ Acesso concedido! Área administrativa.
        <div style="margin-top:0.5rem;font-size:0.8rem">
          <strong>Dados sensíveis:</strong> DUNO{auth_bypass_success}<br/>
          Usuários cadastrados, tokens de API, logs de auditoria...
        </div>
        {% else %}
        ❌ Acesso negado. Você não tem permissão.
        {% endif %}
      </div>
      <p style="font-size:0.82rem;color:var(--text-muted)">Seu role atual: <code>{{ current_user.role }}</code></p>''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Sem verificação — qualquer usuário tem acesso{% endif %}
        {% if level == 'medium' %}Verifica cookie <code>admin=1</code> — adicione via DevTools: Application → Cookies{% endif %}
        {% if level == 'high' %}Verifica sessão role — manipulável se a sessão for forjada{% endif %}
        {% if level == 'impossible' %}Verifica role diretamente no banco por user_id da sessão — sem confiar em cliente{% endif %}
      </div>''',
))

# open_redirect
write("open_redirect", base_template(
    "open_redirect", "16", "Open HTTP Redirect", "↗️",
    "Redirecionamento controlado pelo usuário",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Redirecione para um site externo. Tente <code>?url=https://evil.com</code>
      </p>
      <form method="GET" action="/open_redirect" id="redirect-form">
        <div class="form-group">
          <label for="url-input">URL destino</label>
          <input type="text" id="url-input" name="url" class="form-control"
                 placeholder="https://example.com" value="{{ request.args.get('url', '') }}" />
        </div>
        <button type="submit" class="btn btn-primary">Redirecionar</button>
      </form>
      <div style="margin-top:1rem;font-size:0.82rem;color:var(--text-muted)">
        O servidor irá redirecionar para a URL informada (observe o comportamento em cada nível).
      </div>''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Qualquer URL aceita — phishing via link legítimo{% endif %}
        {% if level == 'medium' %}Bloqueia <code>http://</code> — bypassável com <code>https://</code>{% endif %}
        {% if level == 'high' %}Verifica host mas não subdomínios — bypassável com <code>//evil.com</code>{% endif %}
        {% if level == 'impossible' %}Whitelist de destinos internos — redirecionamento externo impossível{% endif %}
      </div>''',
))

# crypto
write("crypto", base_template(
    "crypto", "17", "Cryptography", "🔑",
    "Dados considerados protegidos — estude as fraquezas de cada abordagem",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Recupere o valor de <code>flag</code>. Analise o esquema criptográfico de cada nível.
      </p>
      <form method="POST" action="/crypto" id="crypto-form">
        <div class="form-group">
          <label for="crypto-key">Chave (secret key)</label>
          <select id="crypto-key" name="key" class="form-control">
            <option value="flag">flag</option>
            <option value="admin_password">admin_password</option>
            <option value="api_key">api_key</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Decodificar</button>
      </form>
      {% if result %}
      <div class="result-box info" style="margin-top:1rem;font-family:monospace">{{ result }}</div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Base64 — encoding, não criptografia. Decodifique com qualquer ferramenta{% endif %}
        {% if level == 'medium' %}XOR com chave fixa (42) — reversível com a mesma operação{% endif %}
        {% if level == 'high' %}MD5 sem salt — vulnerável a rainbow tables{% endif %}
        {% if level == 'impossible' %}pbkdf2:sha256 com salt aleatório — não reversível{% endif %}
      </div>''',
))

# api_versioning
write("api_versioning", base_template(
    "api_versioning", "18", "API Versioning", "📡",
    "Acesso a dados sensíveis via versão de API obsoleta",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Acesse tokens via <code>v1</code>. Em high, envie header <code>X-API-Version: v1</code>.
      </p>
      <form method="GET" action="/api_versioning" id="version-form">
        <div class="form-group">
          <label for="version-select">Versão da API</label>
          <select id="version-select" name="version" class="form-control"
                  onchange="this.form.submit()">
            <option value="v1" {% if version == 'v1' %}selected{% endif %}>v1 (legada)</option>
            <option value="v2" {% if version == 'v2' %}selected{% endif %}>v2 (atual)</option>
          </select>
        </div>
      </form>
      {% if result %}
      <div style="margin-top:1rem;overflow-x:auto">
        <table class="data-table">
          <thead><tr><th>ID</th><th>User ID</th><th>Token</th><th>Version</th></tr></thead>
          <tbody>
            {% for row in result %}
            <tr>
              <td>{{ row.get('id','') }}</td>
              <td>{{ row.get('user_id','') }}</td>
              <td><code>{{ row.get('token','') }}</code></td>
              <td><span class="level-badge level-{% if row.get('version') == 'v1' %}low{% else %}high{% endif %}">{{ row.get('version','') }}</span></td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Sem filtro — retorna todos os tokens independente de versão{% endif %}
        {% if level == 'medium' %}Filtra por versão mas v1 ainda acessível pela URL{% endif %}
        {% if level == 'high' %}Header X-API-Version controla — v1 ainda funcional{% endif %}
        {% if level == 'impossible' %}v1 desativado, filtra por user da sessão, apenas campos não-sensíveis{% endif %}
      </div>''',
))

# mass_assignment
write("mass_assignment", base_template(
    "mass_assignment", "19", "Mass Assignment", "📋",
    "Manipulação de campos via JSON — elevação de privilégio",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Eleve seu role para <code>admin</code>. Em low, envie <code>{"username":"hacker","role":"admin"}</code>
      </p>
      <form method="POST" action="/mass_assignment" id="ma-form">
        <div class="form-group">
          <label for="payload">JSON Payload</label>
          <textarea id="payload" name="payload" class="form-control" rows="4"
                    placeholder='{"username": "hacker", "role": "admin"}'></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Enviar</button>
      </form>
      {% if result %}
      <div class="result-box {% if result.get('error') %}error{% else %}success{% endif %}">
        <pre>{{ result | tojson(indent=2) }}</pre>
      </div>
      {% endif %}''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}Aceita qualquer campo incluindo <code>role</code> e <code>password_hash</code>{% endif %}
        {% if level == 'medium' %}Remove <code>role</code> mas aceita <code>password_hash</code> — ainda perigoso{% endif %}
        {% if level == 'high' %}Apenas <code>username</code> aceito mas sem validação de formato{% endif %}
        {% if level == 'impossible' %}Whitelist estrita + regex de formato — sem injeção de campos internos{% endif %}
      </div>''',
))

# api_security
write("api_security", base_template(
    "api_security", "20", "API Security", "🔌",
    "Laboratório de segurança de API REST — IDOR, JWT, Rate Limit",
    '''      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:1rem">
        <strong style="color:var(--text-primary)">Objetivo:</strong>
        Acesse dados de outro usuário (IDOR). Em low, acesse <code>?user_id=1</code> sendo user 2.
      </p>
      <form method="GET" action="/api_security" id="api-form">
        <div class="form-group">
          <label for="api-uid">User ID alvo</label>
          <input type="number" id="api-uid" name="user_id" class="form-control"
                 placeholder="1" value="{{ target_id }}" min="1" />
        </div>
        <button type="submit" class="btn btn-primary">Consultar</button>
      </form>
      {% if result %}
      <div class="result-box {% if result.get('error') %}error{% else %}success{% endif %}" style="margin-top:1rem">
        <pre>{{ result | tojson(indent=2) }}</pre>
      </div>
      {% endif %}
      <div style="margin-top:1rem;font-size:0.82rem;color:var(--text-muted)">
        Seu user_id: <code>{{ current_user.id }}</code>
      </div>''',
    '''      <div class="alert alert-{% if level == 'impossible' %}success{% elif level == 'high' %}warning{% else %}error{% endif %}">
        {% if level == 'low' %}IDOR sem autenticação — qualquer user_id retorna dados{% endif %}
        {% if level == 'medium' %}Exige autenticação mas sem ownership check — IDOR autenticado{% endif %}
        {% if level == 'high' %}Verifica ownership mas admin vê tudo — privilege escalation{% endif %}
        {% if level == 'impossible' %}Verifica ownership estritamente — apenas seus próprios dados{% endif %}
      </div>
      <div style="margin-top:0.75rem">
        <p style="font-size:0.8rem;color:var(--text-muted)">Endpoints REST disponíveis (via API Security module):</p>
        <ul style="font-size:0.8rem;color:var(--text-secondary);margin-top:0.4rem;padding-left:1.2rem">
          <li>GET /api/users/&lt;id&gt; — IDOR</li>
          <li>POST /api/login — JWT</li>
          <li>GET /api/secrets — dados sensíveis</li>
        </ul>
      </div>''',
))

print("\n[done] Templates gerados.")
