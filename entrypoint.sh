#!/usr/bin/env bash
set -uo pipefail
DATA=/var/lib/pasarguard
mkdir -p "$DATA/node-certs" /var/lib/pg-node
export PORT=8080   # fixed: set the Railway domain target port to 8080

# owner admin/admin is written into the DB by bootstrap.py on every boot
unset SUDO_USERNAME SUDO_PASSWORD

# ---- node secrets: generated once, kept on the volume ----
[ -f "$DATA/node_api_key" ] || python -c "import uuid;print(uuid.uuid4())" > "$DATA/node_api_key"
if [ ! -f "$DATA/node-certs/cert.pem" ]; then
  openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 3650 \
    -keyout "$DATA/node-certs/key.pem" -out "$DATA/node-certs/cert.pem" \
    -subj "/CN=localhost" -addext "subjectAltName=IP:127.0.0.1,DNS:localhost" >/dev/null 2>&1
fi

# ---- nginx ----
sed "s/__PORT__/${PORT}/g" /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
nginx -t || exit 1

# ---- node (xray) ----
( cd /opt/pg-node && \
  SERVICE_PORT=62050 NODE_HOST=127.0.0.1 SERVICE_PROTOCOL=grpc \
  API_KEY="$(cat $DATA/node_api_key)" \
  SSL_CERT_FILE="$DATA/node-certs/cert.pem" SSL_KEY_FILE="$DATA/node-certs/key.pem" \
  exec ./main ) &
NODE_PID=$!

# ---- panel ----
( cd /code && python -m alembic upgrade head && exec python main.py ) &
PANEL_PID=$!

# ---- auto setup (core, node, group, hosts, templates, first user) ----
( cd /code && python bootstrap.py ) &

nginx -g 'daemon off;' &
NGINX_PID=$!

wait -n $NODE_PID $PANEL_PID $NGINX_PID
echo "a process exited, restarting container"; exit 1
