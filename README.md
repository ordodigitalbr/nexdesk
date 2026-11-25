# NexDesk — ISO Debian 13 + KDE Plasma com visual estilo "desktop mode"

Projeto `live-build` que gera uma ISO bootável (BIOS e UEFI) com:

- Debian 13 (Trixie), amd64
- KDE Plasma customizado, tema claro pastel: dock flutuante e arredondado no centro (lançador de apps em tela cheia + apps fixados), bandeja + relógio em uma pílula flutuante à direita, botões de janela (minimizar/maximizar/fechar) no canto direito, papel de parede próprio
- Google Chrome como navegador padrão (baixado do site oficial do Google durante o build)
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

Pelo GitHub Actions (sem precisar de máquina potente): suba esta pasta para um repositório
público no GitHub, abra a aba **Actions → Build ISO → Run workflow** e, ao terminar
(30 a 90 min), baixe o artefato `nexdesk-iso` (vem em .zip com a ISO dentro).

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
  etc/opt/chrome/policies/    políticas do Google Chrome
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

- A sessão no modo live é **Plasma Wayland** em hardware real (exigência do Android/Waydroid) e **X11 dentro de VMs**, onde o Wayland costuma falhar. Para forçar uma delas, no menu de boot aperte TAB e acrescente `nexdesk.x11` ou `nexdesk.wayland`.
- No sistema instalado pelo Calamares o login automático não existe (a tela de login normal é usada).
- Atalhos de janela do Plasma já ajudam a lembrar o desktop mode: `Meta+←/→` encaixa janelas nas metades da tela, `Alt+Tab` alterna janelas.
- Apps Android: veja a seção abaixo.
- Não usa nome, ícones ou assets da Samsung: o visual é "inspirado em", com identidade própria.

## Android e Play Store (Waydroid)

O menu tem o atalho **Configurar Android (Play Store)**. Ele baixa a imagem do Android com serviços do Google
(~1 GB, não pode vir dentro da ISO por causa da licença), inicia o Android e mostra o ID do aparelho, que
precisa ser registrado em https://www.google.com/android/uncertified para o login na Play Store funcionar.

Requisitos e limites:
- Funciona em **computador de verdade** (pendrive ou instalado), com sessão Wayland. Dentro de VM o Android tende a não iniciar ou ficar muito lento.
- Alguns apps só existem para ARM e não rodam; bancos e jogos podem recusar aparelhos não certificados.

## Google Chrome

O Chrome não está nos repositórios do Debian: o build baixa o `.deb` oficial em
`dl.google.com` (precisa de internet no build, o que o GitHub Actions tem). O pacote cadastra o
repositório do Google, e o Chrome se atualiza junto com o sistema.
Uso pessoal: se for **distribuir a ISO publicamente**, confira antes os termos de redistribuição do Chrome.
