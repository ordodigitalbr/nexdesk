#!/bin/sh
# Testa a ISO em uma VM QEMU. Uso: ./run-qemu.sh [arquivo.iso]
ISO="${1:-$(ls ./*.iso 2>/dev/null | head -n1)}"
[ -f "$ISO" ] || { echo "ISO não encontrada. Passe o caminho como argumento." >&2; exit 1; }

KVM=""
[ -w /dev/kvm ] && KVM="-enable-kvm -cpu host"

exec qemu-system-x86_64 $KVM \
	-m 4096 -smp 4 \
	-cdrom "$ISO" -boot d \
	-device virtio-vga \
	-display gtk \
	-device virtio-net-pci,netdev=n0 -netdev user,id=n0 \
	-audiodev pa,id=snd0 -device intel-hda -device hda-duplex,audiodev=snd0
