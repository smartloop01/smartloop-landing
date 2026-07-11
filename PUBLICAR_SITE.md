# Publicar SmartLoop Landing

## Opcao recomendada: Render

1. Crie uma conta em https://render.com
2. Envie esta pasta para um repositorio no GitHub.
3. No Render, clique em **New +**.
4. Escolha **Blueprint** se quiser usar o arquivo `render.yaml`.
5. Conecte o repositorio do GitHub.
6. Configure a variavel secreta:

```text
OPENAI_API_KEY=sua-chave-openai
```

7. Publique.

O Render vai usar:

```text
buildCommand: pip install -r requirements.txt
startCommand: python main.py
```

## Testar local antes de publicar

```powershell
cd "C:\Users\SmarLoop\Documents\Pagina SmartLoop\SmartLoop_Landing_Separado"
python main.py
```

Abra:

```text
http://127.0.0.1:8088
```

## Importante

A chave da OpenAI nao deve ficar dentro do codigo. Configure `OPENAI_API_KEY` na hospedagem.

O banco `leads.db` funciona localmente, mas em hospedagens gratuitas pode ser apagado quando o servidor reinicia. Para producao, o ideal e trocar por banco online.
