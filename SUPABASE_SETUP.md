# Configurar Supabase na SmartLoop

## 1. Criar a tabela

No Supabase, abra:

```text
SQL Editor > New query
```

Cole o conteudo do arquivo:

```text
supabase_schema.sql
```

Depois clique em:

```text
Run
```

## 2. Pegar as chaves

No Supabase, abra:

```text
Project Settings > API
```

Copie:

```text
Project URL
anon public key
```

## 3. Configurar localmente no Windows

No PowerShell:

```powershell
setx SUPABASE_URL "SUA_PROJECT_URL"
setx SUPABASE_KEY "SUA_ANON_PUBLIC_KEY"
```

Feche e abra o terminal novamente.

## 4. Configurar no Render

No Render:

```text
Service > Environment > Add Environment Variable
```

Adicione:

```text
SUPABASE_URL
SUPABASE_KEY
```

Depois faca:

```text
Manual Deploy > Deploy latest commit
```

## 5. Como funciona no codigo

O formulario chama:

```text
lead_service.py
```

Se `SUPABASE_URL` e `SUPABASE_KEY` existirem, salva no Supabase.

Se nao existirem ou se o Supabase falhar, salva no SQLite local `leads.db` como backup.
