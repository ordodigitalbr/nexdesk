#!/bin/sh
# Build dentro de um container Debian 13 (use em qualquer Linux com Docker,
# ou WSL2 com Docker). Resultado: nexdesk-amd64.hybrid.iso nesta pasta.
set -e
cd "$(dirname "$0")"

docker run --rm --privileged \
	-v "$PWD":/work -w /work \
	debian:trixie \
	sh -c 'apt-get update && apt-get install -y sudo && ./build.sh'
