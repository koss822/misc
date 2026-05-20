#!/usr/bin/env bash
# RAM Monitor — installation script
# Tested on Ubuntu 22.04 / 24.04
# Requirements: python3, nginx, openssl, systemd

set -euo pipefail

DOMAIN="ram.local"
PORT="7777"
USER="$(whoami)"
HOME_DIR="$(eval echo ~$USER)"
INSTALL_DIR="$HOME_DIR/ram-monitor"
CERT_DIR="$HOME_DIR/.certs/$DOMAIN"
CA_CRT="$HOME_DIR/ca/rootCA.crt"
CA_KEY="$HOME_DIR/ca/rootCA.key"
CA_SRL="$HOME_DIR/ca/rootCA.srl"

echo "==> RAM Monitor installer"
echo "    User:        $USER"
echo "    Install dir: $INSTALL_DIR"
echo "    Domain:      https://$DOMAIN"
echo ""

# --- 1. Copy application files ---
echo "==> Copying application files to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp "$(dirname "$0")/server.py"  "$INSTALL_DIR/server.py"
cp "$(dirname "$0")/index.html" "$INSTALL_DIR/index.html"

# --- 2. SSL certificate ---
echo "==> Generating SSL certificate for $DOMAIN"
mkdir -p "$CERT_DIR"
cd "$CERT_DIR"

openssl genrsa -out "$DOMAIN.key" 2048 2>/dev/null
openssl req -new -key "$DOMAIN.key" -out "$DOMAIN.csr" -subj "/CN=$DOMAIN" 2>/dev/null
echo "subjectAltName=DNS:$DOMAIN" > "$DOMAIN.ext"

if [[ -f "$CA_CRT" && -f "$CA_KEY" ]]; then
    echo "    Using internal root CA: $CA_CRT"
    openssl x509 -req -in "$DOMAIN.csr" -CA "$CA_CRT" -CAkey "$CA_KEY" \
        -CAserial "$CA_SRL" -out "$DOMAIN.crt" -days 825 -extfile "$DOMAIN.ext" 2>/dev/null
else
    echo "    Internal CA not found — generating self-signed certificate"
    openssl x509 -req -in "$DOMAIN.csr" -signkey "$DOMAIN.key" \
        -out "$DOMAIN.crt" -days 825 -extfile "$DOMAIN.ext" 2>/dev/null
    echo "    NOTE: Add $DOMAIN.crt to your browser's trusted certificates."
fi
cd - > /dev/null

# --- 3. systemd service ---
echo "==> Installing systemd service"
sudo tee /etc/systemd/system/ram-monitor.service > /dev/null << EOF
[Unit]
Description=RAM Monitor (D3.js sunburst dashboard)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now ram-monitor
echo "    Service status: $(systemctl is-active ram-monitor)"

# --- 4. nginx virtual host ---
echo "==> Configuring nginx"
sudo tee /etc/nginx/sites-available/ram > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate     $CERT_DIR/$DOMAIN.crt;
    ssl_certificate_key $CERT_DIR/$DOMAIN.key;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ram /etc/nginx/sites-enabled/ram
sudo nginx -t
sudo systemctl reload nginx

# --- 5. /etc/hosts ---
echo "==> Adding $DOMAIN to /etc/hosts"
if ! grep -q "$DOMAIN" /etc/hosts; then
    echo "127.0.0.1 $DOMAIN" | sudo tee -a /etc/hosts > /dev/null
fi

echo ""
echo "==> Done! Open https://$DOMAIN in your browser."
echo "    (Make sure your browser trusts $CERT_DIR/$DOMAIN.crt)"
