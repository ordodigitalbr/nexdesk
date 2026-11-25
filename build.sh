#!/bin/sh
# Build direto num Debian/Ubuntu (precisa de root). Resultado: nexdesk-amd64.hybrid.iso
set -e
cd "$(dirname "$0")"

if [ "$(id -u)" -ne 0 ]; then
	echo "Rode com sudo: sudo ./build.sh" >&2
	exit 1
fi

apt-get update
apt-get install -y live-build debootstrap squashfs-tools xorriso \
	grub-pc-bin grub-efi-amd64-bin mtools dosfstools python3-pil python3-numpy

python3 tools/make-wallpaper.py

chmod +x auto/config auto/build auto/clean \
	config/hooks/normal/*.hook.chroot \
	config/includes.chroot/lib/live/config/* \
	config/includes.chroot/usr/local/bin/*

lb clean --purge 2>/dev/null || true
lb config
lb build

ls -lh ./*.iso
