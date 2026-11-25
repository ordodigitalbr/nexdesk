// Layout inicial do Plasma, estilo "desktop mode":
//  - dock flutuante, arredondado e centralizado (lançador + apps fixados/abertos)
//  - bandeja do sistema + relógio em uma pílula flutuante à direita

function novoPainel(alinhamento) {
    var p = new Panel();
    p.location = "bottom";
    p.height = 2 * Math.floor(gridUnit * 3.2 / 2);
    p.hiding = "none";
    p.floating = true;
    p.lengthMode = "fit";
    p.alignment = alinhamento;
    return p;
}

// ---------- Dock central ----------
var dock = novoPainel("center");

var launcher = dock.addWidget("org.kde.plasma.kickerdash");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "view-app-grid");
launcher.writeConfig("useCustomButtonImage", true);
launcher.writeConfig("customButtonImage", "view-app-grid");

dock.addWidget("org.kde.plasma.marginsseparator");

var tasks = dock.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", [
    "applications:google-chrome.desktop",
    "applications:org.kde.dolphin.desktop",
    "applications:org.kde.konsole.desktop",
    "applications:org.kde.kate.desktop",
    "applications:systemsettings.desktop"
]);

// ---------- Bandeja + relógio ----------
var bandeja = novoPainel("right");
bandeja.addWidget("org.kde.plasma.systemtray");

var clock = bandeja.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", true);
clock.writeConfig("dateFormat", "shortDate");

// ---------- Papel de parede ----------
var desktopsArray = desktopsForActivity(currentActivity());
for (var i = 0; i < desktopsArray.length; i++) {
    var d = desktopsArray[i];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    d.writeConfig("Image", "file:///usr/share/backgrounds/nexdesk/default.png");
}
