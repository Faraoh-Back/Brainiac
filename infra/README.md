# Infraestrutura

Os arquivos baseados na configuração recebida da EC2 estão na raiz:

- `../docker-compose.yml`, com senhas/tokens substituídos por referências ao `.env`.
- `../nginx/nginx.conf`, com configuração de proxy, domínios de exemplo e caminhos SSL.
- `../docs/CONFIGURACAO.md`, com diferenças e campos que precisam ser preenchidos localmente.

Ainda falta documentar o procedimento real de emissão/renovação de certificados, registrar os digests das imagens e testar uma restauração.

Não incluir `.env`, `ssl/`, chaves PEM, `qr.png`, bancos, sessões ou cópias dos volumes no Git. As chaves SSL podem ser reemitidas; backups privados necessários ficam em armazenamento seguro separado.

Na VM, `bash scripts/coletar_inventario.sh ~/segundo-cerebro` coleta nomes/versões dos serviços, imagens, volumes e nomes das variáveis de ambiente, sem ler os valores dessas variáveis.
