---
title: "Omarchy sur MacBook Pro : l'expérience Arch Linux sans friction sur Apple T2"
date: 2026-09-06T10:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Installer Arch Linux sur un MacBook T2 relevait du sacerdoce. Avec Omarchy, tout est fonctionnel dès le premier boot, avec zéro configuration post-install."
categories: ["Linux", "Hardware", "Tooling"]
tags: ["omarchy", "arch", "macbook", "apple", "hyprland", "linux", "hardware", "dotfiles"]
cover:
  image: /images/covers/omarchy-macbook-pro.webp
  alt: "Omarchy sur MacBook Pro"
---

### L'étincelle : réveiller le hardware Apple

J'ai toujours eu un faible pour le hardware Apple. Le châssis unibody en aluminium taillé au millimètre, l'écran Retina aux couleurs impeccables, le trackpad Force Touch dont la précision reste inégalée dans le monde PC : sur le plan mécanique, ces machines sont des chefs-d'œuvre industriels. 

Dans un précédent article sur la [renaissance des Macs Intel en homelab](/fr/posts/intel-mac-homelab/), je racontais comment j'avais redonné vie à un Mac Pro 2013 et un Mac Mini 2018 sous Fedora et Windows. Mais pour mon laptop portable, le constat devenait frustrant : au fil des versions récentes de macOS, la télémétrie s'accumule, le système se verrouille, et des machines dotées d'une puissance brute considérable finissent bridées par des choix logiciels qui ne correspondent plus à un workflow axé sur le terminal, la CLI et les agents autonomes.

L'étincelle est venue d'un partage d'expérience de Pierre Guillemot ([@pgllmt sur X](https://x.com/pgllmt/status/2096538975443841345)). En voyant ses retours sur la fluidité d'**Omarchy** sur machine Mac et le plaisir de retrouver un environnement Linux ultra-affûté sur du hardware Apple, j'ai eu envie de tester l'aventure sur mon propre **MacBook Pro 15 pouces**.

La promesse semblait presque trop belle : une distribution Arch Linux moderne avec Hyprland, prête à l'emploi, où l'installation sur Mac ne relève plus du parcours du combattant. J'ai branché une clé USB, lancé l'installeur, et ce qui s'est passé a dépassé toutes mes attentes.

---

### Le traumatisme historique : Linux sur MacBook T2

Pour comprendre pourquoi l'expérience Omarchy est un petit miracle d'ingénierie, il faut se rappeler ce que signifiait installer Linux sur un MacBook équipé de la **puce de sécurité Apple T2** (modèles 2018 à 2020).

Sur ces machines (comme mon MacBookPro15,3 avec son Core i9-9980HK, son GPU AMD Radeon Pro Vega 20 et ses 32 Go de RAM), la puce T2 n'est pas un simple coprocesseur de chiffrement :
- Elle fait office de pont PCIe et de contrôleur de bus interne. Le clavier et le trackpad interne sont reliés en USB virtuel via la T2.
- Elle pilote l'accès au SSD NVMe interne (avec chiffrement matériel).
- Elle gère les flux audio (DSP, micros, amplificateurs des haut-parleurs) et la caméra FaceTime HD.
- Elle contrôle le ventilateur et les capteurs thermiques SMC.

Dans une installation Linux classique sur Mac T2, le scénario habituel ressemblait à un cauchemar :
1. **Périphériques muets à l'installation :** sans noyau patché spécifique (`linux-t2`), ni le clavier interne ni le trackpad ne répondent dès l'écran de boot.
2. **Le piège du Wi-Fi Broadcom :** le chipset Wi-Fi Broadcom BCM4364 tente de décharger le 4-way handshake WPA en matériel, ce qui échoue systématiquement sur les réseaux modernes en transition WPA2/WPA3. Le symptôme classique : NetworkManager rejette votre mot de passe en boucle en prétendant qu'il est incorrect.
3. **Le silence radio :** l'audio ne sort pas sur les haut-parleurs sans une batterie de firmwares propriétaires et des profils ALSA/PipeWire sur mesure.
4. **La turbine incontrôlable :** les ventilateurs tournent soit à 100 % en continu (un réacteur d'avion sur le bureau), soit ne se déclenchent pas du tout, risquant la surchauffe du Core i9.

Pour faire tourner Arch Linux proprement, il fallait auparavant jongler avec le dépôt `arch-wiki-docs`, compiler des modules DKMS à la main, configurer manuellement l'initramfs et prier à chaque mise à jour de noyau.

---

### L'approche Omarchy : la détection matérielle "Omakase"

C'est ici qu'**Omarchy** change radicalement la donne. La distribution créée par David Heinemeier Hansson (DHH) applique le principe japonais de l'*omakase* (« je m'en remets à vous ») : un ensemble d'opinions architecturales fortes, cohérentes, polies et prêtes à l'emploi. 

Mais au-delà de sa couche graphique (compositor Wayland Hyprland, shell réactif sous Quickshell, Neovim préconfiguré), Omarchy intègre une suite de scripts de détection matérielle d'une efficacité redoutable.

Pendant la phase d'installation, Omarchy interroge les identifiants PCI de la machine. Dès qu'il repère la signature de la puce Apple T2 (`106b:1801` ou `106b:1802`), le système d'installation prend les choses en main automatiquement :

```bash
# Extrait du script hardware d'Omarchy (/usr/share/omarchy/install/hardware/apple/fix-t2.sh)
if lspci -nn | grep "106b:180[12]" >/dev/null; then
  echo "Detected MacBook with T2 chip. Installing support items..."

  omarchy-pkg-add \
    linux-t2 \
    linux-t2-headers \
    apple-t2-audio-config \
    apple-bcm-firmware \
    t2fanrd
...
```

En une seule passe transparente :
- **Kernel adapté :** installation immédiate du noyau `linux-t2` (actuellement en version 7.1.8-arch1-Watanare-T2) et de ses headers.
- **Initramfs configuré :** injection des modules requis (`t2bce_vhci`, `usbhid`, `hid_apple`) dans `mkinitcpio.conf.d/apple-t2.conf` pour garantir que le clavier et le trackpad soient reconnus dès la saisie de déverrouillage du disque.
- **Gestion thermique silencieuse :** activation de `t2fanrd.service`, un démon moderne écrit en Rust qui régule la courbe de ventilation de manière dynamique selon les capteurs de température du T2.
- **Correctif Wi-Fi automatique :** détection de la carte Broadcom et désactivation du supplicant firmware (`options brcmfmac feature_disable=0x82000`) dans `/etc/modprobe.d/brcmfmac.conf`, confiant le handshake à `wpa_supplicant` logiciel. Fini les faux rejets de mot de passe Wi-Fi.
- **Bootloader Limine :** ajout des paramètres de boot indispensables (`intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep`) pour une mise en veille et un réveil sans accroc.

Vous n'avez rien eu à chercher, rien eu à compiler, aucun forum à éplucher.

---

### Le premier boot : zéro surprise, tout fonctionne

Le moment de vérité arrive au redémarrage. Pas de clé de secours, pas d'écran noir, pas de panique. 

La machine démarre sur le bootloader Limine, charge le kernel T2 et affiche l'interface Omarchy en une poignée de secondes. Et là, l'inventaire du matériel donne le sourire :

| Composant | Statut sous Omarchy | Notes techniques |
| :--- | :--- | :--- |
| **Clavier & Rétroéclairage** | 🟢 Fonctionnel 100% | Rétroéclairage piloté via `apple::kbd_backlight` |
| **Trackpad Force Touch** | 🟢 Fonctionnel 100% | Clic physique haptique, gestes multitouch fluides |
| **Wi-Fi 802.11ac** | 🟢 Fonctionnel 100% | Broadcom BCM4364 connecté instantanément |
| **Bluetooth** | 🟢 Fonctionnel 100% | Démon `hci_bcm4377` actif |
| **Audio & Haut-parleurs** | 🟢 Fonctionnel 100% | PipeWire 1.6 + `apple-t2-audio-config`, son stéréo puissant |
| **Caméra FaceTime HD** | 🟢 Fonctionnel 100% | Détectée nativement via le pilote `uvcvideo` |
| **Dual GPU (Intel + AMD Vega 20)** | 🟢 Fonctionnel 100% | Rendu Wayland direct sous `amdgpu` et Vulkan 1.4 |
| **Écran Retina 2880x1800** | 🟢 Fonctionnel 100% | Densité de pixels magnifique, zéro tearing |
| **Ventilation & Thermique** | 🟢 Fonctionnel 100% | Géré en arrière-plan par le démon Rust `t2fanrd` |

Même la Touch Bar s'initialise correctement avec son rétroéclairage actif (`appletb_backlight`) et ses touches de fonction opérationnelles.

---

### Ce que j'ai configuré après l'installation ? Littéralement 5 lignes

Dans la plupart des aventures Linux sur laptop, le post-install représente 80 % du temps : régler le scaling d'affichage, corriger la disposition du clavier, chercher pourquoi le son craque ou pourquoi la veille vide la batterie en deux heures.

Ici, ma configuration personnelle s'est résumée à **deux fichiers** dans `~/.config/hypr/`.

D'abord, adapter la disposition pour le clavier AZERTY physique d'Apple et activer le défilement naturel dans `~/.config/hypr/input.lua` :

```lua
hl.config({
  input = {
    -- Clavier AZERTY Macintosh sur le clavier ISO intégré
    kb_layout = "fr",
    kb_variant = "mac",
    kb_model = "applealu_iso",
    kb_options = "compose:caps,shift:both_capslock_cancel",

    touchpad = {
      -- Défilement naturel style Mac
      natural_scroll = true,
      clickfinger_behavior = true,
    },
  },
})

-- Balayage horizontal à 3 doigts pour changer de workspace
hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })
```

Ensuite, ajuster le facteur d'échelle pour l'écran Retina 15" dans `~/.config/hypr/monitors.lua` :

```lua
local omarchy_monitor_scale = 1.25

hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })
```

C'est tout. Rien d'autre. Pas de script obscur, pas de bidouillage d'udev rules, pas de patch ALSA expérimental. En 3 minutes chrono, la machine était prête pour le travail quotidien.

---

### Le résultat : une machine de dev ultra-véloce

Sur ce MacBook Pro doté d'un Core i9 8 cœurs / 16 threads et de 32 Go de mémoire vive, Omarchy procure une sensation de légèreté stupéfiante. 

Au repos, l'environnement Wayland consomme à peine 5 Go de RAM avec mes terminaux ouverts, mes outils CLI, btop et les services en arrière-plan. La réactivité d'Hyprland combinée à la dalle Retina donne l'impression d'avoir acheté une machine neuve :
- **Zéro latence :** le passage d'un workspace à l'autre au clavier ou au geste 3 doigts est instantané.
- **Silence absolu :** le démon `t2fanrd` maintient les ventilateurs sous les 2800 tr/min en usage bureautique et dev, éliminant la surchauffe intempestive que macOS provoquait avec ses indexations perpétuelles.
- **Workflow centré sur la CLI :** Neovim, Kitty, Ghostty et mes agents tournent dans un environnement sans distraction, parfaitement aligné avec ma philosophie du [Moindre Privilège](/fr/posts/securing-ai-agents/).

### Conclusion

Si vous possédez un MacBook Intel qui dort dans un tiroir ou dont l'expérience sous macOS s'est dégradée au fil des ans, l'époque où installer Linux était synonyme de nuits blanches est officiellement révolue.

Omarchy prouve qu'une distribution peut être à la fois radicalement axée sur la performance et le contrôle, tout en offrant une expérience d'installation digne d'un système grand public. Le hardware Apple retrouve sa noblesse : une carrosserie d'exception au service d'un moteur Linux libre, rapide et sans compromis.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
