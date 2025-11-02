# Rootless BuildKit Daemon Setup with RootlessKit on Ubuntu

This repository provides an example configuration and setup guide for running BuildKit as a rootless daemon on Ubuntu using RootlessKit. Running BuildKit in rootless mode improves security by avoiding the need for elevated privileges while still delivering the powerful features of BuildKit for container image building. This guide covers installing dependencies, downloading binaries, configuring systemd services, and enabling the daemon.

## Overview

BuildKit is a modern, efficient container image build engine. Running it rootless with RootlessKit allows unprivileged users to run BuildKit securely and conveniently. This setup includes example configuration files and instructions to get your BuildKit daemon up and running with systemd support.

***

## Installation Steps

### 1. Update packages and install prerequisites

```bash
sudo apt update
sudo apt install -y uidmap dbus-user-session curl
```

These packages support user namespaces, systemd user sessions, and downloading files.

***

### 2. Create a dedicated user for BuildKit

```bash
sudo useradd -m -s /bin/bash buildkituser
```

This user will own the BuildKit daemon process and files.

***

### 3. Download and install BuildKit

- Visit the official BuildKit GitHub releases page: https://github.com/moby/buildkit/releases
- Download the latest Linux binary tarball, e.g., `buildkit-v0.x.x.linux-amd64.tar.gz`
- Extract and copy the `buildkitd` binary to `/opt/buildkit/bin/`:

```bash
sudo mkdir -p /opt/buildkit/bin
sudo tar -C /opt/buildkit/bin -xzf buildkit-v0.x.x.linux-amd64.tar.gz buildkitd
sudo chown -R buildkituser:buildkituser /opt/buildkit
sudo chmod +x /opt/buildkit/bin/buildkitd
```


***

### 4. Download and install RootlessKit

RootlessKit enables running processes as an unprivileged user with isolated namespaces.

```bash
# Download latest RootlessKit binary from GitHub releases:
curl -Lo rootlesskit https://github.com/rootless-containers/rootlesskit/releases/download/v0.x.x/rootlesskit-x86_64
sudo mv rootlesskit /usr/local/bin/
sudo chmod +x /usr/local/bin/rootlesskit
```

Adjust `v0.x.x` and architecture as necessary.

***

### 5. Install the example configuration files

- Copy the included `buildkitd.toml` to `/opt/buildkit/` owned by `buildkituser`:

```bash
sudo cp buildkitd.toml /opt/buildkit/
sudo chown buildkituser:buildkituser /opt/buildkit/buildkitd.toml
```

- Copy the `buildkit.service` systemd unit file to manage the daemon, for system-wide or user-level systemd:

```bash
# For system-wide service (root privileges required):
sudo cp buildkit.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now buildkit

# OR, for user-level service (run as buildkituser):
sudo cp buildkit.service /etc/systemd/user/
sudo -u buildkituser systemctl --user daemon-reload
sudo -u buildkituser systemctl --user enable --now buildkit
```


***

### 6. Verify BuildKit daemon status

```bash
sudo systemctl status buildkit
# or, if running as user service
sudo -u buildkituser systemctl --user status buildkit
```


***

## Notes

- Adjust paths (`/opt/buildkit`), usernames, and permissions according to your environment.
- The socket permissions are set to allow easy client connections.
- RootlessKit is required to isolate namespaces and enable rootless execution securely.
- Customize `buildkitd.toml` for more advanced configuration such as logging, storage, or gRPC options.

***

This setup equips you with a secure, rootless BuildKit daemon that can be integrated into CI/CD pipelines or local development environments without requiring root privileges.