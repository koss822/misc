# RPi Backup Script with LVM support - Complete Documentation

## Overview (Perex)
**Automated backup script for Raspberry Pi over SSH.** Backs up:
- **Boot partition** (`/dev/sda1` FAT32) bitwise via `dd`
- **Root filesystem** (`rpi.vg-root`) via LVM snapshot
- **ZFS pool** (`zfspool`) via ZFS snapshot
- **Partition table** (`/dev/sda`)

**Features:**
- Automatic rotation: 2× weekly + 2× monthly backups
- Systemd timer for scheduling
- Email reports after each backup
- LVM/ZFS snapshot cleanup

---

## Asciinema
[![asciicast](https://asciinema.org/a/767417.svg)](https://asciinema.org/a/767417)

## Requirements

### On backup host (linux)
```bash
# Dependencies
sudo apt install pv mailutils openssh-client

# SSH config (~/.ssh/config)
Host rpi.home
    HostName rpi.home
    User youruser
    StrictHostKeyChecking no
```


### On RPi (rpi.home)

```bash
# LVM + ZFS + sfdisk
sudo apt install lvm2 zfsutils-linux

# SSH keys
ssh-copy-id youruser@rpi.home
```


---

## Script Installation

```bash
# Save script
chmod +x ~/backup-rpi.sh

# Test run
./backup-rpi.sh rpi.home

# Target directory (must exist)
sudo mkdir -p /mnt/linux-share/backups/rpi/{weekly,monthly}
sudo chown youruser:youruser /mnt/linux-share/backups/rpi
```


---

## Systemd Timer (root)

### 1. Service: `/etc/systemd/system/backup-rpi.service`

```ini
[Unit]
Description=RPi Automated Backup
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=mkonicek
WorkingDirectory=/home/mkonicek
ExecStart=/home/mkonicek/backup-rpi.sh
```


### 2. Timer: `/etc/systemd/system/backup-rpi.timer`

```ini
[Unit]
Description=Weekly RPi Backup
Requires=backup-rpi.service

[Timer]
OnCalendar=Mon *-*-* 03:00:00
Persistent=true

[Install]
WantedBy=multi-user.target
```


### 3. Enable \& Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup-rpi.timer
sudo systemctl status backup-rpi.timer
sudo systemctl list-timers | grep backup
```


---

## Backup Directory Structure

```
/mnt/linux-share/backups/rpi/
├── weekly/2026-01-02/     ← First week
│   ├── rpi_boot.img.gz
│   ├── rpi_root.tar.gz
│   ├── rpi_zfspool.tar.gz
│   └── rpi_ptable.sfdisk
├── monthly/2026-01/       ← Full month
└── ... (max 2 per type)
```


---

## Restore from Backups

### 1. Partition Table

```bash
sudo sfdisk /dev/sda < rpi_ptable.sfdisk
```


### 2. Boot (FAT32)

```bash
sudo dd if=rpi_boot.img.gz | gunzip | dd of=/dev/sda1 bs=4M
```


### 3. Rootfs

```bash
# Create LV
sudo lvcreate -n root_restore -L 50G rpi.vg
sudo mkfs.ext4 /dev/rpi.vg/root_restore
sudo mount /dev/rpi.vg/root_restore /mnt/restore

# Restore tar
sudo tar -xzf rpi_root.tar.gz -C /mnt/restore --numeric-owner
```


### 4. ZFS Pool

```bash
sudo zfs create -o mountpoint=/zfspool zfspool
sudo tar -xzf rpi_zfspool.tar.gz -C /zfspool
sudo chown -R mkonicek:mkonicek /zfspool
```


---

## Cleanup Scripts

### LVM Root Cleanup

```bash
# Included in backup-rpi.sh as lvm_root_cleanup_remote()
```

## Monitoring \& Logs

```bash
# Timer status
sudo systemctl status backup-rpi.{timer,service}

# Last run logs
sudo journalctl -u backup-rpi.service -n 100

# Email reports
sudo tail -f /var/mail/root
```

## Script Code Reference

### Main Variables

```bash
RPI_HOST="${1:-rpi.home}"
BASE_BACKUP_DIR="/mnt/linux-share/backups/rpi"
BOOT_BACKUP="rpi_boot.img.gz"
ROOT_BACKUP="rpi_root.tar.gz"
ZFSP_BACKUP="rpi_zfspool.tar.gz"
PTABLE_BACKUP="rpi_ptable.sfdisk"
```


### Backup Rotation Logic

```bash
DAY_OF_MONTH=$(date +%d)
if [ $DAY_OF_MONTH -le 7 ]; then
  BACKUP_TYPE="weekly"
  BACKUP_DIR="$BASE_BACKUP_DIR/$BACKUP_TYPE/$(date +%Y-%m-%U)"
else
  BACKUP_TYPE="monthly"
  BACKUP_DIR="$BASE_BACKUP_DIR/$BACKUP_TYPE/$(date +%Y-%m)"
fi
```


### Boot Backup Example

```bash
ssh "$RPI_HOST" "sudo blockdev --getsize64 /dev/sda1 > $RPI_TEMP/boot-size"
SIZE=$(ssh "$RPI_HOST" "sudo cat '$RPI_TEMP/boot-size'")
ssh "$RPI_HOST" "sudo dd if=/dev/sda1 bs=4M status=none" | \
  pv -s $SIZE | gzip > "./$BOOT_BACKUP"
```


### LVM Snapshot Cleanup

```bash
lvm_root_cleanup_remote() {
ssh "$RPI_HOST" sudo bash << 'EOF'
  echo "=== Cleaning root-backup-* LVM snapshots ==="
  
  # Unmount
  mount | grep "root--backup-" | awk '{print $3}' | sort -u | while read mnt; do
    umount "$mnt" 2>/dev/null || true
  done
  
  # Remove LVs
  lvs | grep "root-backup-" | awk '{print $1}' | while read lv; do
    lvremove -f "/dev/rpi.vg/$lv" 2>/dev/null || true
  done
EOF
}
```


### Email Report

```bash
REPORT=$(cat <<EOF
$(echo "✅ Done: $BACKUP_DIR")
$(ls -lh *.img *.tar.gz *.sfdisk 2>/dev/null)
$(du -sh "$BACKUP_DIR")
EOF
)

echo "$REPORT" | mail -s "RPi backup report: $BACKUP_DIR" root
```
