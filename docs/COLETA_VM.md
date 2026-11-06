# Arquivos que precisamos da EC2

## Já recebido

- Compose e configuração do Nginx.
- Serviços em execução, versão do n8n e confirmação de SQLite.
- Volume efetivo do n8n: segundo-cerebro_n8n_data.

## Ainda falta enviar

| Arquivo | Como preparar |
|---|---|
| `.env.example` | Enviar somente os nomes das variáveis, sem os valores. Comando abaixo. |
| Pipeline principal | Já recebida em 05/11/2026; envie novamente somente se houver alterações posteriores. |
| JSON do Cobrador | Enviar se esse workflow existir na instalação atual. |
| Outros workflows ativos | Exportar para completar o inventário do projeto. |

O briefing v3 corrigido já está no projeto; envie uma nova exportação somente se você alterou a versão importada.

## Inventário sem valores secretos

Execute na EC2 e envie as saídas:

```bash
cd ~/segundo-cerebro
docker compose ps -a
docker compose version
docker exec n8n n8n --version
docker exec n8n sh -c 'printf "DB_TYPE=%s\n" "${DB_TYPE:-sqlite}"'
docker inspect n8n --format '{{range .Mounts}}{{println .Type .Name .Source "->" .Destination}}{{end}}'
```

Isso identifica serviços, versão do n8n, tipo de banco e onde seus dados são montados. Não imprime a lista completa de variáveis do container.

Para criar uma lista das variáveis sem divulgar seus valores:

```bash
cd ~/segundo-cerebro
if [ -f .env ]; then
  awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1 "="}' .env > /tmp/brainiac.env.example
fi
```

Envie `/tmp/brainiac.env.example`, não o `.env` original. O comando não modifica o arquivo em produção.

## Não enviar ao chat nem ao Git

- `.env` original e `N8N_ENCRYPTION_KEY` real.
- `nginx/ssl/*_privkey.pem`, chave SSH PEM e demais chaves privadas.
- `nginx/qr.png` e dados de sessão do WhatsApp.
- Export de credenciais em texto aberto, dumps de bancos e cópias dos volumes.

A pasta `nginx/ssl/` inteira fica fora do Git. Os certificados públicos não são necessários para o versionamento; documentaremos a reemissão/renovação.

O `.env` pode estar presente mesmo sem aparecer no `tree`, pois arquivos com ponto inicial não aparecem por padrão. Os bancos provavelmente estão em volumes Docker ou bind mounts e, por isso, também podem não aparecer nessa árvore. Sua localização será confirmada pelo inventário.

## Etapas depois da coleta

1. Conferir as diferenças do Compose/Nginx públicos em CONFIGURACAO.md.
2. Adicionar exports atuais das pipelines em commits próprios.
3. Definir destino privado e independente para backups de estado, com criptografia.
4. Testar restauração em outro ambiente.
