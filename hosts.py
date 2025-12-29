#!/usr/bin/python3
import subprocess
from pathlib import Path

base = {
    ".zshrc": "~/",
    "init.lua": "~/.config/nvim/",
}

x = base | {
    ".fehbg": "~/",
    "config.rasi": "~/.config/rofi/",
    "alacritty.toml": "~/.config/alacritty/",
    "sxhkdrc": "~/.config/sxhkd/",
    "bspwmrc": "~/.config/bspwm/",
    ".xinitrc": "~/",
    "poweroff.desktop": "~/.local/share/applications/",
    "picom.conf": "~/.config/picom/",
    "polybar-parts": "~/.config/polybar/config.ini",
}

allowed = {"X": x, "Base (no x)": base}

requirements = ["feh", "bspwm", "sxhkd", "polybar", "neovim", "alacritty", "picom", "rofi", "zsh", "xserver-xorg", "xinit", "firefox-esr", "python3-pip", "python3-venv", "zeal", "brightnessctl"]

def render_polybar():
    power_supps = Path("/sys/class/power_supply").iterdir()
    batteries = [p.name for p in power_supps if p.name.startswith("BAT")]

    start = open("configs/polybar-parts/start").read()
    mid = open("configs/polybar-parts/mid").read()
    end = open("configs/polybar-parts/end").read()

    rendered = start.strip()
    rendered += "\nmodules-right = " + " ".join(b.lower() for b in batteries)
    rendered += mid
    for batt in batteries:
        rendered += f"\n[module/{batt.lower()}]"
        rendered += "\ninherit = module/battery"
        rendered += "\nbattery = " + batt + "\n"
    rendered += end

    return rendered


def ask_user(allowed):
    print("Available configs:")

    for i, a in enumerate(allowed):
        print(f"{i}. {a}")

    chosen = input("Select config [0]: ").strip()

    if chosen == "":
        chosen = 0

    try:
        chosen_idx = int(chosen)
        key = list(allowed.keys())[chosen_idx]
        return allowed[key]

    except (ValueError, IndexError):
        return ask_user(allowed)

def install(name, destination, dry_run):
    dest_path = Path(destination).expanduser()

    if destination.endswith("/"):
        dest_path /= name

    source_path = Path("configs") / name
    
    if name == "polybar-parts":
        rendered = render_polybar()
        source_lines = rendered.splitlines()
    else:
        rendered = False
        with open(source_path) as f:
            source_lines = f.read().splitlines()

    if dest_path.exists():
        with open(dest_path) as f:
            dest_lines = f.read().splitlines()
    else:
        dest_lines = []

    if source_lines == dest_lines:
        print("No change: ", source_path, "->", dest_path)
    else:
        print("Change: ", source_path, "->", dest_path)

    if not dry_run:
        subprocess.run(("mkdir", "-p", str(dest_path.parent)))
        if rendered:
            with open(dest_path, "w") as f:
                f.write(rendered)
        else:
            subprocess.run(("cp", str(source_path), str(dest_path)))

dry_run = input("Dry run? [Y/n]").strip().lower()

if dry_run == "":
    dry_run = "y"

dry_run = dry_run == "y"

chosen = ask_user(allowed) 

for name, dest in chosen.items():
    install(name, dest, dry_run)

subprocess.run(("mkdir", "-p", "~/Documents/zeal-docsets"))
subprocess.run(("ln", "-s", "~/Documents/zeal-docsets", "~/.local/share/Zeal/Zeal/docsets"))

subprocess.run(("sudo", "apt-get", "update"))

apt_install = ["sudo", "apt-get", "install"] + requirements

if dry_run:
    apt_install.insert(3, "--dry-run")
else:
    apt_install.insert(3, "-y")

subprocess.run(apt_install)


