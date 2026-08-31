#!/usr/bin/env bash
set -euo pipefail

# Runs ON the VM (scp'd there by the deploy workflow, executed via SSH).
# Fetches app secrets directly from Secret Manager using the VM's own
# attached service account via the metadata server — secrets never pass
# through the GitHub Actions runner, its logs, or the SSH command line.

PROJECT_ID="$1"
DOMAIN="$2"
IMAGE="$3"
SECRET_PREFIX="$4" # e.g. stackport-staging / stackport-production

# Not `cd ~/stackport`: this runs under `sudo`, which resets $HOME to
# root's, not the OS Login user's home the files actually live in.
cd "$(dirname "$0")"

TOKEN=$(curl -sf -H "Metadata-Flavor: Google" \
  "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" \
  | jq -r .access_token)

fetch_secret() {
  local secret_id="$1"
  curl -sf -H "Authorization: Bearer ${TOKEN}" \
    "https://secretmanager.googleapis.com/v1/projects/${PROJECT_ID}/secrets/${secret_id}/versions/latest:access" \
    | jq -r .payload.data | base64 -d
}

SUPABASE_URL=$(fetch_secret "${SECRET_PREFIX}-supabase-url")
SUPABASE_ANON_KEY=$(fetch_secret "${SECRET_PREFIX}-supabase-anon-key")
SUPABASE_SERVICE_ROLE_KEY=$(fetch_secret "${SECRET_PREFIX}-supabase-service-role-key")

umask 077
cat > .env <<EOF
DOMAIN=${DOMAIN}
IMAGE=${IMAGE}
SUPABASE_URL=${SUPABASE_URL}
SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
EOF

docker compose pull
docker compose up -d --remove-orphans
