#!/usr/bin/env bash
#
# setup-lxqt-vnc.sh — Install LXQt desktop + TigerVNC + noVNC + nginx (HTTPS)
#                      on Ubuntu 24.04, running as the current (non-root) user.
#
# Usage:
#   chmod +x setup-lxqt-vnc.sh
#   ./setup-lxqt-vnc.sh
#
# The script will ask for:
#   - VNC password
#   - Root CA certificate and key file paths (to sign the domain certificate)
#   - Domain name for the nginx HTTPS reverse proxy
#
# All services run as the current user. sudo is used only where root is required.
#

set -euo pipefail

# ─── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
err()   { echo -e "${RED}[ERROR]${NC} $*" >&2; }
fatal() { err "$@"; exit 1; }

# ─── Pre-flight checks ────────────────────────────────────────────────────────
[[ $(id -u) -ne 0 ]] || fatal "Do NOT run this script as root. Run it as your regular user — sudo is used internally where needed."
command -v sudo >/dev/null 2>&1 || fatal "sudo is not installed."
command -v openssl >/dev/null 2>&1 || { info "openssl not found, will be installed."; }

CURRENT_USER="$(id -un)"
CURRENT_HOME="$HOME"

# ─── Banner ───────────────────────────────────────────────────────────────────
echo -e "${BOLD}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   LXQt + VNC + nginx Setup for Ubuntu 24.04          ║${NC}"
echo -e "${BOLD}║   Running as: ${CURRENT_USER}                                   ${NC}${BOLD}║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════╝${NC}"
echo

# ─── User prompts ─────────────────────────────────────────────────────────────
read -rp "VNC password (min 6 chars): " -s VNC_PASSWORD
echo
[[ ${#VNC_PASSWORD} -ge 6 ]] || fatal "VNC password must be at least 6 characters."

read -rp "VNC resolution [1920x1080]: " VNC_RES
VNC_RES="${VNC_RES:-1920x1080}"

echo
echo -e "${BOLD}--- SSL / Domain setup ---${NC}"
echo "You need a root CA certificate + key to sign the domain certificate."
echo "Example files: /home/${CURRENT_USER}/ca/rootCA.crt  /home/${CURRENT_USER}/ca/rootCA.key"
echo

read -rp "Path to root CA certificate file (e.g. /home/${CURRENT_USER}/ca/rootCA.crt): " ROOT_CA_CRT
[[ -f "$ROOT_CA_CRT" ]] || fatal "Root CA certificate not found: $ROOT_CA_CRT"

read -rp "Path to root CA key file (e.g. /home/${CURRENT_USER}/ca/rootCA.key): " ROOT_CA_KEY
[[ -f "$ROOT_CA_KEY" ]] || fatal "Root CA key not found: $ROOT_CA_KEY"

read -rp "Domain name for the VNC web interface (e.g. vnc.home.lan): " DOMAIN
[[ -n "$DOMAIN" ]] || fatal "Domain name cannot be empty."

echo
info "Configuration summary:"
echo "  Current user:   ${CURRENT_USER}"
echo "  VNC resolution: ${VNC_RES}"
echo "  Root CA cert:   ${ROOT_CA_CRT}"
echo "  Root CA key:    ${ROOT_CA_KEY}"
echo "  Domain:         ${DOMAIN}"
echo
read -rp "Proceed? [y/N]: " CONFIRM
[[ "${CONFIRM,,}" == "y" ]] || { echo "Aborted."; exit 0; }

# ─── Install system packages ──────────────────────────────────────────────────
info "Updating package lists..."
sudo apt-get update -q

info "Installing LXQt, TigerVNC, noVNC, nginx, and supporting tools..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    lxqt openbox lxterminal \
    tigervnc-standalone-server \
    novnc websockify \
    nginx \
    openssl \
    dbus-x11 \
    fonts-noto-color-emoji \
    xdg-utils
ok "Packages installed."

# ─── Configure VNC ────────────────────────────────────────────────────────────
info "Configuring TigerVNC..."
mkdir -p "${CURRENT_HOME}/.config/tigervnc"

echo "${VNC_PASSWORD}" | vncpasswd -f > "${CURRENT_HOME}/.config/tigervnc/passwd"
chmod 600 "${CURRENT_HOME}/.config/tigervnc/passwd"

cat > "${CURRENT_HOME}/.config/tigervnc/xstartup" << 'XSTARTUP'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec dbus-launch --exit-with-session startlxqt
XSTARTUP
chmod +x "${CURRENT_HOME}/.config/tigervnc/xstartup"
ok "TigerVNC configured."

# ─── Disable LXC/VM-incompatible LXQt autostart entries ──────────────────────
info "Disabling power management and screensaver autostart entries..."
mkdir -p "${CURRENT_HOME}/.config/autostart"

cat > "${CURRENT_HOME}/.config/autostart/lxqt-powermanagement.desktop" << 'NOAUTO'
[Desktop Entry]
Type=Application
Name=LXQt Power Management
Hidden=true
NOAUTO

cat > "${CURRENT_HOME}/.config/autostart/lxqt-xscreensaver-autostart.desktop" << 'NOAUTO'
[Desktop Entry]
Type=Application
Name=LXQt Screen Saver
Hidden=true
NOAUTO
ok "Autostart entries disabled."

# ─── Configure LXQt default terminal ─────────────────────────────────────────
info "Setting lxterminal as default terminal in LXQt..."
mkdir -p "${CURRENT_HOME}/.config/lxqt"
cat > "${CURRENT_HOME}/.config/lxqt/session.conf" << 'CONF'
[General]
__userfile__=true

[Environment]
TERM=xterm-256color

[Preferred Applications]
terminal_emulator=lxterminal
CONF
ok "LXQt session configured."

# ─── Configure lxterminal (dark theme) ───────────────────────────────────────
info "Configuring lxterminal with dark theme..."
mkdir -p "${CURRENT_HOME}/.config/lxterminal"
cat > "${CURRENT_HOME}/.config/lxterminal/lxterminal.conf" << 'CONF'
[general]
fontname=Monospace 12
bgcolor=#1e1e2e
fgcolor=#cdd6f4
palette_color_0=#45475a
palette_color_1=#f38ba8
palette_color_2=#a6e3a1
palette_color_3=#f9e2af
palette_color_4=#89b4fa
palette_color_5=#f5c2e7
palette_color_6=#94e2d5
palette_color_7=#bac2de
palette_color_8=#585b70
palette_color_9=#f38ba8
palette_color_10=#a6e3a1
palette_color_11=#f9e2af
palette_color_12=#89b4fa
palette_color_13=#f5c2e7
palette_color_14=#94e2d5
palette_color_15=#a6adc8
scrollback=10000
CONF
ok "lxterminal configured."

# ─── Set noVNC default scaling to auto ────────────────────────────────────────
NOVNC_UI="/usr/share/novnc/app/ui.js"
if [[ -f "$NOVNC_UI" ]]; then
    sudo sed -i "s/UI.initSetting('resize', 'off')/UI.initSetting('resize', 'scale')/" "$NOVNC_UI" 2>/dev/null || true
fi

# ─── Generate SSL certificate signed by root CA ───────────────────────────────
info "Generating SSL certificate for domain: ${DOMAIN}..."
CERT_DIR="${CURRENT_HOME}/.certs/${DOMAIN}"
mkdir -p "$CERT_DIR"

# Generate private key + CSR
openssl genrsa -out "${CERT_DIR}/${DOMAIN}.key" 2048

openssl req -new \
    -key "${CERT_DIR}/${DOMAIN}.key" \
    -out "${CERT_DIR}/${DOMAIN}.csr" \
    -subj "/CN=${DOMAIN}"

# Create SAN extension file
cat > "${CERT_DIR}/${DOMAIN}.ext" << EXTFILE
subjectAltName=DNS:${DOMAIN}
EXTFILE

# Sign with the provided root CA
openssl x509 -req \
    -in "${CERT_DIR}/${DOMAIN}.csr" \
    -CA "${ROOT_CA_CRT}" \
    -CAkey "${ROOT_CA_KEY}" \
    -CAcreateserial \
    -out "${CERT_DIR}/${DOMAIN}.crt" \
    -days 825 \
    -extfile "${CERT_DIR}/${DOMAIN}.ext"

chmod 600 "${CERT_DIR}/${DOMAIN}.key"
ok "Certificate generated: ${CERT_DIR}/${DOMAIN}.crt"

# ─── Configure nginx ─────────────────────────────────────────────────────────
info "Configuring nginx reverse proxy for ${DOMAIN}..."

sudo tee /etc/nginx/sites-available/novnc > /dev/null << NGINXCONF
server {
    listen 80;
    server_name ${DOMAIN};
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name ${DOMAIN};

    ssl_certificate     ${CERT_DIR}/${DOMAIN}.crt;
    ssl_certificate_key ${CERT_DIR}/${DOMAIN}.key;

    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    # noVNC web interface
    location / {
        proxy_pass http://127.0.0.1:6080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_read_timeout 86400;
    }
}
NGINXCONF

# Enable site
sudo ln -sf /etc/nginx/sites-available/novnc /etc/nginx/sites-enabled/novnc
# Remove default site if it exists (to avoid port 80 conflict)
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx
ok "nginx configured and running."

# ─── Create systemd user services ─────────────────────────────────────────────
info "Creating systemd user services..."
mkdir -p "${CURRENT_HOME}/.config/systemd/user"

# VNC service
cat > "${CURRENT_HOME}/.config/systemd/user/vncserver.service" << SVCD
[Unit]
Description=TigerVNC Server (display :1)
After=network.target

[Service]
Type=forking
Environment=HOME=${CURRENT_HOME}
ExecStartPre=/bin/sh -c "/usr/bin/vncserver -kill :1 > /dev/null 2>&1 || :"
ExecStart=/usr/bin/vncserver :1 -geometry ${VNC_RES} -depth 24 -localhost yes -rfbauth ${CURRENT_HOME}/.config/tigervnc/passwd
ExecStop=/usr/bin/vncserver -kill :1
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
SVCD

# noVNC / websockify service
cat > "${CURRENT_HOME}/.config/systemd/user/novnc.service" << 'SVCD'
[Unit]
Description=noVNC WebSocket Proxy
After=vncserver.service
Requires=vncserver.service

[Service]
Type=simple
ExecStart=/bin/websockify --web=/usr/share/novnc/ 6080 localhost:5901
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
SVCD

ok "Systemd user service files created."

# ─── Enable lingering (so user services start on boot without login) ──────────
info "Enabling lingering for user '${CURRENT_USER}'..."
sudo loginctl enable-linger "${CURRENT_USER}"
ok "Lingering enabled."

# ─── Enable and start services ────────────────────────────────────────────────
info "Enabling and starting VNC + noVNC services..."
systemctl --user daemon-reload
systemctl --user enable vncserver.service novnc.service
systemctl --user start vncserver.service
sleep 3
systemctl --user start novnc.service
ok "Services started."

# ─── Verify services ──────────────────────────────────────────────────────────
info "Verifying services..."
for svc in vncserver novnc; do
    if systemctl --user is-active --quiet "$svc"; then
        ok "$svc is running."
    else
        warn "$svc failed to start. Check with: systemctl --user status $svc"
    fi
done

if systemctl is-active --quiet nginx; then
    ok "nginx is running."
else
    warn "nginx failed to start. Check with: sudo systemctl status nginx"
fi

# ─── Print summary ────────────────────────────────────────────────────────────
echo
echo -e "${BOLD}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Setup Complete!                                    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════╝${NC}"
echo
echo -e "  ${BOLD}Remote Desktop (noVNC):${NC}"
echo -e "    https://${DOMAIN}/vnc.html"
echo -e "    VNC password: (the password you entered)"
echo
echo -e "  ${BOLD}Certificate files:${NC}"
echo -e "    Cert: ${CERT_DIR}/${DOMAIN}.crt"
echo -e "    Key:  ${CERT_DIR}/${DOMAIN}.key"
echo
echo -e "  ${BOLD}Manage services:${NC}"
echo -e "    systemctl --user status vncserver"
echo -e "    systemctl --user status novnc"
echo -e "    sudo systemctl status nginx"
echo
echo -e "  ${BOLD}Next step — trust the root CA on your client machine:${NC}"
echo -e "    Copy ${ROOT_CA_CRT} to your Windows/Linux/macOS machine"
echo -e "    and add it to the trusted root certificate store."
echo -e "    See the README.md in this directory for instructions."
echo
