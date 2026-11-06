# Publicar SmartLuup no Google Cloud Run

O projeto usa Flet dinamico e precisa de um servidor Python com WebSocket. O `Dockerfile` inicia `main.py` na porta `PORT` informada pelo Cloud Run.

## Preparar a conta

1. Crie um projeto no Google Cloud Console e vincule uma conta de faturamento. A cota gratuita nao impede cobranças acima dela.
2. Crie um alerta de orçamento no Billing antes de publicar. O alerta nao bloqueia gastos.

## Publicar o site

1. Abra Cloud Run no Console e clique em **Connect repository**.
2. Escolha o repositorio GitHub `smartloop01/smartloop-landing` e a branch `smartloop-landing`.
3. Escolha a compilacao por `Dockerfile` na raiz do repositorio.
4. Use o nome `smartluup`, regiao `us-east1`, acesso publico, porta `8080`, minimo `0` e maximo `1` instancia. Aumente o timeout para ate `3600` segundos para as conexoes WebSocket.
5. Adicione as variaveis `SUPABASE_URL`, `SUPABASE_KEY` e `REQUIRE_SUPABASE=1`. Para o agente, adicione `OPENAI_API_KEY` e, se necessario, `OPENAI_MODEL`.
6. Aguarde a compilacao e teste a URL `*.run.app`, o formulario e o agente. Confirme que um lead novo aparece no Supabase.

## Dominio

1. A regiao `us-east1` aceita o mapeamento direto de dominio do Cloud Run, mas esse recurso ainda e Preview. No Console, abra Cloud Run > Domain mappings e adicione `www.smartluup.com.br` ao servico `smartluup`.
2. Verifique a propriedade de `smartluup.com.br` quando solicitado. Use os registros de verificacao e DNS exatos que o Google mostrar.
3. Na Locaweb, substitua o CNAME `www` antigo do Render pelo destino dado pelo Google. Nao altere o DNS antes de testar a URL `*.run.app`.
4. Para que `smartluup.com.br` sem `www` tambem abra, crie um segundo mapeamento no Cloud Run para o dominio raiz e substitua o registro A antigo do Render pelos registros exatos que o Google mostrar. Os dois enderecos servirao o site; esse mapeamento nao cria um redirecionamento automatico para `www`.

Nao coloque chaves de API no GitHub. O SQLite local nao e persistente no Cloud Run; o formulario deve usar Supabase. Conexoes WebSocket ativas consomem recursos e podem gerar custos acima da cota gratuita.
