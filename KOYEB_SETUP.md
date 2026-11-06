# Publicar SmartLuup no Koyeb

1. Crie uma conta em https://app.koyeb.com/ e conecte o GitHub `smartloop01`.
2. Crie um **Web Service** a partir de `smartloop01/smartloop-landing`, branch `smartloop-landing`.
3. Escolha **Buildpack**, instância **Free** e uma região oferecida para ela. Deixe o diretório raiz vazio. O `Procfile` inicia `python main.py`.
4. Exponha uma porta HTTP (por exemplo, `8000`). O Koyeb define `PORT` automaticamente para a porta exposta; o `main.py` escuta nessa porta em `0.0.0.0`.
5. Cadastre as variáveis de ambiente `SUPABASE_URL`, `SUPABASE_KEY` e `REQUIRE_SUPABASE=1`. Use `SUPABASE_TABLE=leads` se a tabela tiver esse nome. Para o agente, cadastre `OPENAI_API_KEY` e, se necessário, `OPENAI_MODEL`.
6. Aguarde o deploy e teste a URL `*.koyeb.app`, inclusive o formulário e o agente. Confirme que o lead aparece no Supabase.
7. No Koyeb, abra **Domains** e adicione `www.smartluup.com.br` ao app. Na Locaweb, substitua o CNAME atual de `www` pelo destino exato que o Koyeb mostrar. Aguarde a validação e o certificado TLS.
8. Depois de confirmar o `www`, configure na Locaweb um redirecionamento HTTP do domínio sem `www` para `https://www.smartluup.com.br`, se a conta oferecer esse recurso. Caso contrario, sera necessario usar um DNS/servico de redirecionamento compativel. O registro A antigo do Render nao faz esse redirecionamento.

Nao coloque chaves no codigo ou no GitHub. A instancia Free pode hibernar e nao tem armazenamento persistente; por isso os leads devem ser salvos no Supabase.
