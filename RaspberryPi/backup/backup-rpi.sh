#!/bin/bash
set -euo pipefail

RPI_HOST="${1:-rpi.home}"
BASE_BACKUP_DIR="/mnt/linux-share/backups/rpi"

DAY_OF_MONTH=$(date +%d)
if [ $DAY_OF_MONTH -le 7 ]; then
  BACKUP_TYPE="weekly"
  BACKUP_DIR="$BASE_BACKUP_DIR/$BACKUP_TYPE/$(date +%Y-%m-%U)"
else
  BACKUP_TYPE="monthly"
  BACKUP_DIR="$BASE_BACKUP_DIR/$BACKUP_TYPE/$(date +%Y-%m)"
fi

BOOT_BACKUP="rpi_boot.img.gz"
ROOT_BACKUP="rpi_root.tar.gz"
ZFSP_BACKUP="rpi_zfspool.tar.gz"
PTABLE_BACKUP="rpi_ptable.sfdisk"

mkdir -p "$BACKUP_DIR"
cd "$BACKUP_DIR"

# Remove old rpi temps
ssh "$RPI_HOST" "rm -rf /tmp/rpi-backup.* 2>/dev/null || true"
# Create new rpi temp
RPI_TEMP=$(ssh "$RPI_HOST" mktemp -d /tmp/rpi-backup.XXXXXX)

lvm_root_cleanup_remote() {
ssh "$RPI_HOST" sudo bash << 'EOF'
  echo "=== Cleaning root-backup-* LVM snapshots ==="

  # 1. Unmount all root-backup-* mounts
  echo "Unmounting root-backup mounts..."
  mount | grep "root--backup-" | awk '{print $3}' | sort -u | while read mnt; do
    echo "  Unmounting: $mnt"
    umount "$mnt" 2>/dev/null || echo "    Warning: $mnt busy/already unmounted"
  done

  # 2. Remove ALL inactive root-backup-* LVs
  echo "Removing inactive root-backup-* LVs..."
  lvs | grep "root-backup-" | awk '{print $1}' | while read lv; do
    echo "  Removing: $lv"
    lvremove -f "/dev/rpi.vg/$lv" 2>/dev/null || echo "    Warning: $lv failed"
  done

  # 3. Cleanup temp dirs
  echo "Cleaning temp root-mnt dirs..."
  rm -rf /tmp/rpi-backup.*/root-mnt 2>/dev/null || true
  rmdir /root-mnt 2>/dev/null || true

  echo "=== Cleanup complete ==="
  echo "Remaining mounts:"
  mount | grep root-backup || echo "  None"
  echo "Remaining LVs:"
  lvs | grep root-backup || echo "  None"
EOF
}

echo "Backing up $RPI_HOST → $BACKUP_DIR ($BACKUP_TYPE)"
echo "RPi temp: $RPI_TEMP"

# Retention: keep 2 newest dirs
find "$BASE_BACKUP_DIR/$BACKUP_TYPE" -maxdepth 1 -type d -printf '%T@ %p\n' | \
  sort -nr | tail -n +3 | cut -d' ' -f2 | xargs -r rm -rf

# 1. Partition table
ssh "$RPI_HOST" "sudo sfdisk -d /dev/sda > '$RPI_TEMP/ptable'"
scp "$RPI_HOST:$RPI_TEMP/ptable" "./$PTABLE_BACKUP"

# 2. Boot partition
echo "Boot backup..."
ssh "$RPI_HOST" "sudo blockdev --getsize64 /dev/sda1 > $RPI_TEMP/boot-size"

SIZE=$(ssh "$RPI_HOST" "sudo cat '$RPI_TEMP/boot-size'")
ssh "$RPI_HOST" "sudo dd if=/dev/sda1 bs=4M status=none" | \
  pv -s $SIZE | gzip > "./$BOOT_BACKUP"

# 3. ROOTFS LVM snapshot
lvm_root_cleanup_remote
echo "Rootfs snapshot..."
SNAP_NAME="root-backup-$(date +%s)"
ssh "$RPI_HOST" sudo bash << EOF
  mkdir -p $RPI_TEMP/root-mnt
  lvcreate -L 10G -s -n $SNAP_NAME /dev/rpi.vg/root
  mount /dev/rpi.vg/$SNAP_NAME $RPI_TEMP/root-mnt
  echo 'Calculating size...'
  du -sb $RPI_TEMP/root-mnt | cut -f1 > $RPI_TEMP/root-size
EOF

SIZE=$(ssh "$RPI_HOST" "sudo cat $RPI_TEMP/root-size")
ssh "$RPI_HOST" "sudo tar -C '$RPI_TEMP/root-mnt' -cz \
  --exclude=proc --exclude=sys --exclude=dev --exclude=tmp --exclude=var/tmp \
  --exclude=run --exclude=lost+found . 2>/dev/null" | \
  pv -s $SIZE | gzip > "./$ROOT_BACKUP"

lvm_root_cleanup_remote

# ZFS Clean
# Unmount all /tmp/rpi-backup.*/zfs-mnt
# Destroy all zfspool@backup-* snapshots
zfs_cleanup() {
ssh "$RPI_HOST" sudo bash << EOF
  echo "Unmounting zfs-mnt mounts..."
  mount | grep "zfs-mnt" | awk '{print \$3}' | while read mnt; do
    echo "Unmounting: \$mnt"
    sudo umount "\$mnt" 2>/dev/null || echo "Warning: \$mnt already unmounted"
  done

  echo "Destroying old snapshots..."
  zfs list -t snapshot -H -o name | grep "^zfspool@backup-" | while read snap; do
    echo "Destroying: \$snap"
    sudo zfs destroy "\$snap" 2>/dev/null || echo "Warning: \$snap busy/invalid"
  done
  rmdir $RPI_TEMP/zfs-mnt 2>/dev/null || true
EOF
}



# 4. ZFS snapshot
zfs_cleanup

echo "ZFS snapshot..."
SNAP_NAME="backup-$(date +%s)"
ssh "$RPI_HOST" sudo bash << EOF
  mkdir -p $RPI_TEMP/zfs-mnt
  zfs snapshot zfspool@$SNAP_NAME
  mount -t zfs zfspool@$SNAP_NAME $RPI_TEMP/zfs-mnt
  echo 'Calculating size...'
  sudo du -sb $RPI_TEMP/zfs-mnt | cut -f1 > $RPI_TEMP/zfs-size
EOF

SIZE=$(ssh "$RPI_HOST" "sudo cat $RPI_TEMP/zfs-size")
ssh "$RPI_HOST" "sudo tar -C $RPI_TEMP/zfs-mnt -cz . 2>/dev/null" | \
  pv -s $SIZE | gzip > "./$ZFSP_BACKUP"

zfs_cleanup

REPORT=$(cat <<EOF
$(echo "✅ Done: $BACKUP_DIR")
$(ls -lh *.img.gz *.tar.gz *.sfdisk 2>/dev/null)
$(du -sh "$BACKUP_DIR")
EOF
)

# Print to screen
echo "$REPORT"

# Email to root
echo "$REPORT" | mail -s "RPi backup report: $BACKUP_DIR" root