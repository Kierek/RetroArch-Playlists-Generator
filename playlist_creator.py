import json
import os
import sys

from modules.gui_resolver import GUIResolver
from modules.no_gui_resolver import NoGUIResolver

default_cores_location = "/usr/lib/libretro/"
default_info_files_location = "/usr/share/libretro/info/"
default_playlists_location = os.path.join(os.path.expanduser("~"), ".config/retroarch/playlists/")

preferences_file_location = (os.path.join(os.path.expanduser("~"), ".config/", "playlists_creator.json"))

systems_list = ("3DO",
                "Atari - 2600",
                "Atari - 7800",
                "Atari - Jaguar",
                "Atari - Lynx",
                "Atari - ST",
                "Bandai - WonderSwan Color",
                "Bandai - WonderSwan",
                "Commodore Amiga",
                "DOOM",
                "DOS",
                "FB Alpha - Arcade Games",
                "GCE - Vectrex",
                "Magnavox - Odyssey2",
                "MAME",
                "Microsoft - MSX",
                "Microsoft - MSX2",
                "NEC - PC Engine - TurboGrafx 16",
                "NEC - PC Engine CD - TurboGrafx-CD",
                "NEC - PC Engine SuperGrafx",
                "NEC - PC-FX",
                "Neo Geo",
                "Nintendo - Famicom Disk System",
                "Nintendo - Game and Watch",
                "Nintendo - Game Boy Advance",
                "Nintendo - Game Boy Color",
                "Nintendo - Game Boy",
                "Nintendo - Nintendo 64",
                "Nintendo - Nintendo DS",
                "Nintendo - Nintendo Entertainment System",
                "Nintendo - Satellaview",
                "Nintendo - Super Nintendo Entertainment System",
                "Nintendo - Virtual Boy",
                "Sega - 32X",
                "Sega - Game Gear",
                "Sega - Master System - Mark III",
                "Sega - Mega Drive - Genesis",
                "Sega - Mega-CD - Sega CD",
                "Sega - Saturn",
                "Sega - SG-1000",
                "Sinclair - ZX Spectrum +3",
                "SNK - Neo Geo Pocket Color",
                "SNK - Neo Geo Pocket",
                "Sony - PlayStation Portable",
                "Sony - PlayStation")


def main(argv):
    if len(argv) > 0:
        for opt in argv:
            if opt == "--nogui":
                start_no_gui()
            else:
                print('usage: playlist._creator.py [arg]')
                print('-h - prints this page')
                print('--nogui - starts the CLI version')
                sys.exit()
    else:
        start_gui()


def start_gui():
    if not os.path.isfile(preferences_file_location):
        __init_prefs()
    GUIResolver()


def start_no_gui():
    NoGUIResolver(default_cores_location).set_system()


def __init_prefs():
    config = {'playlists_location': default_playlists_location,
              'cores_location': default_cores_location,
              'infos_location': default_info_files_location}

    with open(preferences_file_location, 'w') as f:
        json.dump([config], f, indent=4)


if __name__ == "__main__":
    main(sys.argv[1:])
