# Recuperação se a EC2 for perdida

O GitHub preserva configurações e definições de workflows. Não preserva automaticamente bancos, credenciais, dados dos volumes nem a sessão do WhatsApp.

## Configuração confirmada da VM

1. Compose e Nginx reais foram recebidos e incorporados ao repositório com segredos e domínios pessoais removidos. Consulte CONFIGURACAO.md para as diferenças.
2. n8n 2.29.10 usa SQLite. O volume confirmado é `segundo-cerebro_n8n_data`, montado em `/home/node/.n8n`. Ele contém o banco e outros arquivos do n8n. Copiar somente os workflows JSON não preserva credenciais e todo esse estado.
3. PostgreSQL 15 atende à Evolution v2.3.7. Banco e usuário configurados: `evolution`. O Compose declara `postgres_data`, `evolution_data` e `redis_data`, além de `n8n_data`; confirme os nomes efetivos com docker inspect antes do backup desses três volumes.
4. Principal e briefing atuais recebidos. Ainda faltam o Cobrador (se existir), os digests das imagens e o procedimento real de renovação SSL. Os JSONs públicos são templates, não cópias completas das configurações privadas.

## O que precisa de cópia segura fora da EC2 e fora do Git

- `.env` e `N8N_ENCRYPTION_KEY` exata da instância. Não gere outra chave para tentar abrir credenciais antigas.
- Volume completo do n8n, incluindo SQLite, credenciais cifradas, estado de publicação, usuários e outros arquivos em `/home/node/.n8n`.
- Banco/estado da Evolution e sessões necessárias. Uma reconexão do WhatsApp pode ser necessária mesmo com backup.
- Dados persistentes de outros serviços, inclusive Redis se houver necessidade de preservar histórico temporário. Memória de uma hora não substitui armazenamento permanente.
- Credenciais externas, DNS e instruções de recuperação de conta.

Defina um destino independente da VM, com criptografia, frequência e retenção. Só uma cópia no disco da própria EC2 pode ser perdida junto com ela. Um backup na mesma conta AWS pode ficar inacessível se a conta for suspensa; avalie manter uma cópia independente.

Para o volume n8n com SQLite, planeje uma parada controlada do n8n durante a cópia ou um snapshot consistente. Copie também os arquivos associados, não só `database.sqlite` durante gravação. A parada causa indisponibilidade do bot e do cron; registre o horário e reinicie após a cópia.

Para o PostgreSQL da Evolution, use dump consistente; preserve também o estado de sessões necessário em evolution_data. Se precisar de um ponto consistente entre banco e sessões, coordene a parada de gravações da Evolution. Não substitua um dump por cópia do diretório PostgreSQL em uso.

Mantenha os arquivos privados cifrados, fora do diretório do repositório e com uma cópia independente da EC2. Ainda não foi executado backup nem configurada transferência externa por este trabalho. Somente os nomes das variáveis são versionados. A encryption key original precisa permanecer em armazenamento privado recuperável.

## Ordem de restauração

1. Preparar novo host, Docker, rede, armazenamento e versões compatíveis das imagens.
2. Clonar o repositório e recuperar os segredos de armazenamento seguro.
3. Restaurar os bancos e volumes adequados, com permissões e a chave n8n original.
4. Subir os serviços; ajustar DNS, HTTPS e endereço de webhook para o novo host.
5. Verificar credenciais Google, Evolution e conexão do WhatsApp; reconectar quando necessário.
6. Confirmar apenas um workflow publicado por agendamento/webhook e testar o Principal.
7. Testar o briefing manual e depois verificar o disparo às 08h.

A recuperação só fica comprovada após um teste em ambiente separado. Este pacote não executou backup de estado nem teste de restauração.
