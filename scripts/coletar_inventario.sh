#!/usr/bin/env bash
# Coleta somente inventário; não copia .env, certificados, bancos ou sessões.
set -euo pipefail
umask 077
compose_dir="${1:-$HOME/segundo-cerebro}"
cd -- "$compose_dir"
out_dir="$(mktemp -d "${TMPDIR:-/tmp}/brainiac-inventario.XXXXXX")"

docker compose version > "$out_dir/compose-version.txt"
docker compose ps -a > "$out_dir/containers.txt"
docker compose config --services > "$out_dir/servicos.txt"
docker compose ps -a -q > "$out_dir/container-ids.txt"
while IFS= read -r container_id; do
  [[ -n "$container_id" ]] || continue
  docker inspect --format 'Nome: {{.Name}}
Imagem configurada: {{.Config.Image}}
Imagem em execucao: {{.Image}}
{{range .Mounts}}Mount: {{.Type}} {{.Name}} {{.Source}} -> {{.Destination}}
{{end}}' "$container_id" >> "$out_dir/volumes-e-imagens.txt"
done < "$out_dir/container-ids.txt"
rm -f -- "$out_dir/container-ids.txt"

if [[ -f .env ]]; then
  awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1 "="}' .env > "$out_dir/env.example"
fi

printf 'Inventário salvo em: %s\n' "$out_dir"
printf 'Revise e envie esses arquivos. O Compose e nginx.conf devem ser enviados separadamente, com segredos removidos.\n'
