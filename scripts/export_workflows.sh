#!/usr/bin/env bash
set -euo pipefail
umask 077

container_name="${1:-n8n}"
export_mode="${2:-}"
if [[ -n "$export_mode" && "$export_mode" != '--published' ]]; then
  echo 'Uso: bash scripts/export_workflows.sh [container] [--published]' >&2
  exit 2
fi
repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
private_dir="$(mktemp -d)"
container_file=''
cleanup() {
  rm -rf -- "$private_dir"
  if [[ -n "$container_file" ]]; then
    docker exec -u node "$container_name" rm -f -- "$container_file" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

container_file="$(docker exec -u node "$container_name" sh -c 'umask 077; mktemp /tmp/brainiac-workflows.XXXXXX.json')"
cmd=(n8n export:workflow --all "--output=$container_file")
if [[ "$export_mode" == '--published' ]]; then cmd+=(--published); fi
docker exec -u node "$container_name" "${cmd[@]}"
docker cp "$container_name:$container_file" "$private_dir/workflows.json"
python3 "$repo_dir/scripts/sanitize_workflows.py" "$private_dir/workflows.json" --public --output "$repo_dir/workflows/exported"
echo 'Exportação concluída. Revise as alterações antes de fazer commit. Nada foi enviado ao GitHub.'
