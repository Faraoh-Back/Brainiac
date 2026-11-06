# Configuração local e diferenças da EC2

## Workflows públicos

Os JSONs deste repositório são templates. Para uma recuperação fiel, prefira os workflows completos guardados em backup privado com as credenciais cifradas e a encryption key original.

Para configurar os templates:

1. Selecione as credenciais Google Calendar, Tasks, Sheets, Gemini, Redis e Evolution que cada workflow usa. Nenhum ID de credencial pessoal é publicado.
2. No início de Resolver Listas do briefing, substitua `CONFIGURAR_NUMERO_WHATSAPP` pelo destinatário com DDI/DDD e sem sinais. Confira os quatro nomes de listas; os IDs são descobertos pela API. Os fallbacks pessoais foram removidos.
3. No Principal, configure o número autorizado em Extrair Dados e a lista correta em cada nó Tasks. O export atual foi recebido em 05/11/2026; as melhorias funcionais pendentes não foram implementadas por este versionamento.
4. Configure `CONFIGURAR_PLANILHA_ID` nos nós Sheets. Calendar aponta por padrão para `primary`; selecione outro calendário se necessário.
5. Substitua `evolution.example.com` nas URLs dos nós HTTP pelo domínio local da Evolution. A credencial Header Auth deve ter Name `apikey` e o valor privado correto.
6. Execute os workflows manualmente e confira resultados. Publique apenas os fluxos desejados; não deixe dois briefings agendados ao mesmo tempo.

O briefing usa Open-Meteo e RSS da Agência Brasil sem chave. Redis mantém o histórico da pipeline principal; não é o banco de credenciais do n8n.

## Compose

Configuração confirmada na EC2: n8n 2.29.10 em SQLite, volume `segundo-cerebro_n8n_data` em `/home/node/.n8n`; Evolution v2.3.7 em PostgreSQL 15; Redis 7 e Nginx Alpine.

Diferenças do arquivo público:

- `name: segundo-cerebro` evita que o nome da pasta do clone crie outro conjunto de volumes por engano.
- n8n foi fixado em `2.29.10` em vez de `latest`, conforme a versão do executável informada. Os demais tags amplos foram mantidos; ainda falta registrar os digests das imagens em uso.
- `DB_TYPE=sqlite` deixa explícito o banco observado.
- A senha literal do PostgreSQL saiu do arquivo. Preencha `POSTGRES_PASSWORD` e `EVOLUTION_DATABASE_CONNECTION_URI` no `.env` local. Para restaurar banco existente, use valores compatíveis com o usuário já gravado no banco.
- A URI tem forma `postgresql://USUARIO:SENHA@postgres:5432/BANCO`. Caracteres reservados da senha devem ser codificados na URI. Não publique a URI real.
- Os mounts Nginx/SSL são somente leitura.
- Os domínios do Nginx foram substituídos por exemplos. O Nginx não lê essas variáveis do `.env` automaticamente; edite seus `server_name` antes de iniciar.

Alterar `POSTGRES_PASSWORD` no Compose não altera a senha de um banco existente. Não gere uma senha nova durante esta migração sem também realizar uma rotação coordenada no banco e na Evolution. Não apague o volume para resolver erro de autenticação.

As portas 5678 e 8080 foram preservadas como na configuração recebida. Confirme as regras de entrada da EC2. A revisão futura pode restringir esses acessos, preservando o Nginx como entrada pública. Nada foi modificado na VM por este versionamento.

## Fontes

- https://hub.docker.com/_/postgres — inicialização das variáveis em diretório de dados vazio.
- https://docs.n8n.io/hosting/cli-commands/ — exportação de workflows/credenciais e backup completo.
