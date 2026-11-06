# Brainiac

Meu assistente pessoal via WhatsApp, com n8n, Evolution API e Redis.

Repositório de código e configuração pública do Brainiac. Não contém os segredos nem o estado privado da VM. A restauração completa ainda precisa ser testada.

## Conteúdo

- `workflows/briefing-matinal-v3.json`: briefing corrigido, agendado às 08h no fuso America/Sao_Paulo. Clima Open-Meteo e notícias RSS da Agência Brasil sem chave. Agenda/tarefas desta semana e da próxima.
- `workflows/principal.json`: exportação atual da pipeline principal recebida em 05/11/2026, convertida em template público. As melhorias funcionais pendentes não foram implementadas nesse snapshot.
- `scripts/export_workflows.sh`: exporta workflows da instalação Docker e produz cópias para revisão antes do commit.
- `scripts/sanitize_workflows.py`: remove dados fixados, estado de execução e segredos explícitos de campos conhecidos. Não é uma auditoria completa de código JavaScript, URLs, textos e dados pessoais.
- `scripts/coletar_inventario.sh`: coleta serviços, imagens, volumes e nomes das variáveis da VM sem copiar os valores das variáveis.
- `docker-compose.yml`: configuração baseada na EC2, com n8n 2.29.10, SQLite e PostgreSQL exclusivo da Evolution. Senhas foram substituídas por variáveis.
- `nginx/nginx.conf`: proxy baseado na EC2, com domínios de exemplo e caminhos SSL.
- `docs/RECUPERACAO.md`: o que o Git cobre e o que precisa de backup externo.
- `docs/PENDENCIAS.md`: validações e trabalho ainda necessário.

Os workflows são templates públicos e inativos. Telefone, conta Google, planilha, IDs de listas e referências de credenciais foram removidos ou substituídos. Importar não publica agendamentos. Veja `docs/CONFIGURACAO.md` antes de usar.

Backups privados são indispensáveis para preservar as configurações completas. Nunca envie ao Git a documentação Master original, `.env`, exports privados ou bancos.

## Organização dos commits

Estrutura, pipeline principal, briefing, scripts, Compose, Nginx e documentação são versionados em commits separados. A infraestrutura da EC2 não é alterada por um commit neste repositório.

## Configurar em outro ambiente

1. Leia `docs/RECUPERACAO.md` e restaure os dados necessários antes de subir os serviços.
2. Copie `.env.example` para `.env` local e preencha os valores privados.
3. Ajuste os dois domínios de exemplo em `nginx/nginx.conf` e restaure/emita os certificados em `nginx/ssl/`.
4. Configure os campos dos templates conforme `docs/CONFIGURACAO.md`, ou restaure os workflows completos de backup privado.
5. Valide `docker compose config --quiet`. Depois de conferir volumes e backups, suba os serviços.

O projeto Compose se chama explicitamente `segundo-cerebro`, preservando o prefixo de volumes confirmado na EC2. Não execute `docker compose down -v` em uma migração: isso remove volumes.

## Exportar a instalação atual da EC2

Copie este repositório para uma máquina com acesso ao Docker da EC2 e execute a partir da raiz do repositório:

```bash
bash scripts/export_workflows.sh n8n
```

O primeiro argumento é o nome do container, que nos arquivos recebidos é `n8n`. O comando não altera os workflows no banco nem os publica: usa a CLI para leitura/exportação e arquivos temporários. Produz templates públicos com configurações removidas. Não é um backup fiel para restauração. Revise `git diff` e `git status` antes do commit.

A exportação padrão contém os rascunhos atuais. Em versões n8n que suportam a opção, use `bash scripts/export_workflows.sh n8n --published` para exportar versões publicadas. Essa opção omite workflows não publicados. Não trate uma exportação apenas dos rascunhos como prova da versão executada em produção.

Os arquivos exportados vão para `workflows/exported/`. Remoções no n8n não apagam arquivos antigos dessa pasta automaticamente; revise arquivos obsoletos antes do commit. O script não faz commit nem push automático.

## Validar o briefing

1. Importe o briefing em workflow novo e vazio e confirme as referências às credenciais Google/WhatsApp.
2. Execute o fluxo inteiro pelo Teste manual e confirme os dados e a entrega real.
3. Desative o briefing antigo; publique/ative o corrigido.
4. Em Executions, confirme a execução automática às 08h e o recebimento no WhatsApp.

Foram feitos testes locais de código e consultas aos serviços públicos de clima/notícias. Não houve acesso à instância n8n, publicação nela nem observação do cron em produção.

## Fontes operacionais

- CLI n8n: https://docs.n8n.io/hosting/cli-commands/
- Backup completo: https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/backup-and-restore/
