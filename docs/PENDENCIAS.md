# Pendências do Brainiac

## Confirmado nesta conversa

- O usuário confirmou anteriormente a recuperação do bot e do Redis.
- A v3 do briefing foi gerada e passou em testes locais; clima/notícias públicos foram consultados com sucesso.
- Não houve acesso ao n8n para confirmar importação, publicação, envio ou disparo automático da v3.

## Prioridade operacional

- Validar briefing manual com dados reais e entrega no WhatsApp.
- Publicar a v3 e confirmar o disparo automático das 08h; verificar histórico de execução se não disparar.
- Compose e Nginx coletados e versionados; Principal e briefing atuais coletados; falta o Cobrador (se existir) e os digests das imagens.
- Guardar bancos/volumes e encryption key fora da EC2 e testar restauração.
- Repositório definido: Faraoh-Back/Brainiac. Manter alterações em commits separados e conferir o estado remoto após cada envio.

## Pipeline principal

- Corrigir e validar datas/conclusão de Tasks e criação/edição/exclusão de eventos Calendar.
- Mapear colunas do Sheets explicitamente e alinhar urgencia/urgente.
- Deduplicar pelo ID original da mensagem; impedir repetição de ações ao recuperar falha de envio.
- Serializar mensagens por conversa e tratar falhas de forma explícita.
- Implementar ramo de membros, identificação da task e atualização de status com permissões por contato.
- Validar/autenticar webhook, tipos de evento, grupos e mensagens vazias.
- Alinhar o prompt às ferramentas efetivamente disponíveis.

## Outros fluxos e manutenção

- Obter e revisar o JSON atual do Cobrador; testar lembretes, frequência, resposta do membro e notificação ao dono.
- Resolver aviso de overcommit do Redis e acompanhar memória/reinícios.
- Validar renovação/aplicação de SSL e reconexão OAuth/WhatsApp.
- Revisar segredos expostos na documentação antiga e substituí-los.
- Planejar a rotação da senha PostgreSQL que estava escrita no Compose, sem quebrar o acesso da Evolution; não confundir variável de inicialização com alteração de senha do usuário existente.
- Recursos futuros: áudio, imagens, busca web, relatórios semanais e lembretes antes de eventos.
