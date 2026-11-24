# NexDesk — ISO Debian 13 + KDE Plasma com visual estilo "desktop mode"

Projeto `live-build` que gera uma ISO bootável (BIOS e UEFI) com:

- Debian 13 (Trixie), amd64
- KDE Plasma customizado: barra de tarefas única embaixo, lançador de apps em tela cheia à esquerda, ícones de apps fixados, bandeja + relógio à direita, botões de janela (minimizar/maximizar/fechar) no canto direito, tema escuro, papel de parede próprio
- Chromium como navegador padrão
- Instalador gráfico Calamares
- Idioma pt_BR, teclado ABNT2 (br), fuso America/Sao_Paulo
- Login automático no modo live (usuário `nexdesk`, senha `live`)

"NexDesk" é um nome provisório. Para trocar: `NAME="MeuSO" ./build.sh` ou edite `auto/config`.

> **Status:** os arquivos foram escritos mas o build **ainda não foi executado**.
> Na primeira rodada podem aparecer ajustes (nome de pacote, opção do live-build).
> Se algo falhar, envie o `build.log`.

## Requisitos para o build

- Debian 13 / Ubuntu 24.04+ (físico ou VM) **ou** qualquer Linux/WSL2 com Docker
- ~25 GB de disco livre, 8 GB de RAM recomendados, internet
- Tempo: 20 a 60 min na primeira vez

## Como gerar a ISO

Direto num Debian/Ubuntu:

```sh
sudo ./build.sh
```

Via Docker:

```sh
./build-docker.sh
```

A ISO aparece na raiz do projeto como `nexdesk-amd64.hybrid.iso`. O log fica em `build.log`.

Para limpar e refazer: `sudo lb clean --purge` e rode o build de novo.

ISO menor (sem pacotes "recomendados"): `APT_RECOMMENDS=false sudo -E ./build.sh`.

## Testar

VM com QEMU:

```sh
./run-qemu.sh nexdesk-amd64.hybrid.iso
```

VirtualBox/VMware: crie uma VM Linux Debian 64-bit, 4 GB de RAM, 2+ CPUs, 64 MB de vídeo, EFI opcional, e monte a ISO.

Pendrive (cuidado: apaga o dispositivo, confira `/dev/sdX` com `lsblk`):

```sh
sudo dd if=nexdesk-amd64.hybrid.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

## Estrutura

```
auto/                         config/build/clean do live-build (opções da ISO)
config/package-lists/         pacotes instalados
config/hooks/normal/          scripts executados dentro do chroot no build
config/includes.chroot/       arquivos copiados para o sistema
  etc/skel/.config/           configs padrão de novos usuários (tema, janelas, mime)
  etc/chromium/policies/      políticas do Chromium
  lib/live/config/            login automático (só no modo live)
  usr/share/plasma/look-and-feel/org.nexdesk.desktop/
                              layout do painel e padrões visuais
tools/make-wallpaper.py       gera o papel de parede (rodado pelo build.sh)
```

## Onde mexer para personalizar

| Quero mudar... | Arquivo |
|---|---|
| Apps fixados na barra | `.../layouts/org.kde.plasma.desktop-layout.js` (`launchers`) |
| Posição/altura da barra, widgets | mesmo arquivo |
| Botões das janelas | `etc/skel/.config/kwinrc` (`ButtonsOnRight`) |
| Cores, ícones, tema | `.../contents/defaults` |
| Papel de parede | `tools/make-wallpaper.py` ou troque `default.png` |
| Pacotes | `config/package-lists/desktop.list.chroot` |
| Idioma/teclado/fuso | `--bootappend-live` em `auto/config` |

## Detalhes e limitações conhecidas

- A sessão padrão é **Plasma X11** (`plasmax11`), mais compatível com VMs. Para Wayland, troque `Session=plasmax11.desktop` por `Session=plasma.desktop` em `config/includes.chroot/lib/live/config/9990-nexdesk-autologin`.
- No sistema instalado pelo Calamares o login automático não existe (a tela de login normal é usada).
- Atalhos de janela do Plasma já ajudam a lembrar o desktop mode: `Meta+←/→` encaixa janelas nas metades da tela, `Alt+Tab` alterna janelas.
- Apps Android (como no DeX) exigem Waydroid, que não está incluído; dá para adicionar depois.
- Não usa nome, ícones ou assets da Samsung: o visual é "inspirado em", com identidade própria.
