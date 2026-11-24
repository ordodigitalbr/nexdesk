// Layout inicial do Plasma: barra de tarefas única na parte inferior,
// com lançador em tela cheia à esquerda e bandeja + relógio à direita.

var panel = new Panel();
panel.location = "bottom";
panel.height = 2 * Math.floor(gridUnit * 3 / 2);
panel.hiding = "none";
panel.floating = false;

// Lançador de apps em tela cheia (grade de apps)
var launcher = panel.addWidget("org.kde.plasma.kickerdash");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "view-app-grid");

panel.addWidget("org.kde.plasma.marginsseparator");

// Apps fixados + janelas abertas (somente ícones)
var tasks = panel.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", [
    "applications:chromium.desktop",
    "applications:org.kde.dolphin.desktop",
    "applications:org.kde.konsole.desktop",
    "applications:org.kde.kate.desktop",
    "applications:systemsettings.desktop"
]);

panel.addWidget("org.kde.plasma.marginsseparator");

// Lado direito: bandeja do sistema, relógio, mostrar área de trabalho
panel.addWidget("org.kde.plasma.systemtray");

var clock = panel.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", true);
clock.writeConfig("dateFormat", "shortDate");

panel.addWidget("org.kde.plasma.showdesktop");

// Papel de parede
var desktopsArray = desktopsForActivity(currentActivity());
for (var i = 0; i < desktopsArray.length; i++) {
    var d = desktopsArray[i];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    d.writeConfig("Image", "file:///usr/share/backgrounds/nexdesk/default.png");
}
