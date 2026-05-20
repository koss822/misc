#!/usr/bin/env bash
# Installs geckodriver + Python dependencies for web-screenshots.
# Tested on Ubuntu 22.04 / 24.04.
# Requires: Firefox >= 78, Python 3.8+

set -euo pipefail

GECKODRIVER_VER="${GECKODRIVER_VER:-0.36.0}"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"

echo "==> Installing Python dependencies"
if command -v pip3 &>/dev/null; then
    pip3 install -r "$(dirname "$0")/requirements.txt" --break-system-packages 2>/dev/null \
      || pip3 install -r "$(dirname "$0")/requirements.txt"
else
    sudo apt-get install -y python3-pip
    pip3 install -r "$(dirname "$0")/requirements.txt" --break-system-packages
fi

echo "==> Downloading geckodriver v${GECKODRIVER_VER}"
ARCH="$(uname -m)"
case "$ARCH" in
    x86_64)  GECKO_ARCH="linux64" ;;
    aarch64) GECKO_ARCH="linux-aarch64" ;;
    *)       echo "Unsupported arch: $ARCH"; exit 1 ;;
esac

curl -sL "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VER}/geckodriver-v${GECKODRIVER_VER}-${GECKO_ARCH}.tar.gz" \
  | tar -xz -C /tmp/

sudo mv /tmp/geckodriver "${INSTALL_DIR}/geckodriver"
sudo chmod +x "${INSTALL_DIR}/geckodriver"

echo "==> geckodriver $(geckodriver --version | head -1)"
echo "==> Done. Test with: python3 screenshot.py https://example.com /tmp/test.png"
