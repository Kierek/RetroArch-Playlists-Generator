import os


class PlaylistGenerator:
    picked_system = None
    roms_dir = None
    core_file = None
    core_name = None

    def __init__(self, default_playlists_location):
        self.default_playlists_location = default_playlists_location

    def set_system(self, picked_system):
        self.picked_system = picked_system

    def set_dir(self, roms_dir):
        self.roms_dir = roms_dir

    def set_core_file(self, core_file):
        self.core_file = core_file

    def set_core_name(self, core_name):
        self.core_name = core_name

    def generate_playlist_file(self, target_dir):
        if self.picked_system is None or self.roms_dir is None:
            print("System or directory not set")
            return

        files = sorted(os.listdir(target_dir))
        new_playlist_file = open(
            os.path.join(self.default_playlists_location, self.picked_system + ".lpl"), "w")
        first = True
        i = 0

        for rom in files:
            if not first:
                new_playlist_file.write("\n")
            else:
                first = False

            # full path
            new_playlist_file.write(os.path.join(target_dir, rom) + "\n")
            # name
            new_playlist_file.write(os.path.splitext(os.path.basename(rom))[0] + "\n")
            # core's path
            if self.core_file is not None:
                new_playlist_file.write(self.core_file + "\n")
            else:
                new_playlist_file.write("DETECT" + "\n")
            # core's name
            if self.core_name is not None:
                new_playlist_file.write(self.core_name + "\n")
            else:
                new_playlist_file.write("DETECT" + "\n")
            # crc placeholder
            new_playlist_file.write("DETECT" + "\n")
            # playlist's name
            new_playlist_file.write(self.picked_system + ".lpl")

            i += 1

        new_playlist_file.close()
        print("Found: {} ROMS for {}".format(i, self.picked_system))

    def start_generator(self):
        self.generate_playlist_file(self.roms_dir)


def fire_generator(playlists_location, roms_dir, picked_system, selected_core, cores_name):
    playlist_generator = PlaylistGenerator(playlists_location)
    playlist_generator.set_dir(roms_dir)
    playlist_generator.set_system(picked_system)
    playlist_generator.set_core_file(selected_core)
    playlist_generator.set_core_name(cores_name)
    playlist_generator.start_generator()


def find_core_name(selected_core_path, info_path):
    # name should be the same as core's, aside from ext
    info_file_name = os.path.splitext(os.path.basename(selected_core_path))[0] + ".info"

    # join .info file path
    selected_cores_info = os.path.join(info_path, info_file_name)

    if os.path.isfile(selected_cores_info):
        with open(selected_cores_info, "r") as f:
            for line in f:
                # line with corename found
                if "corename" in line:
                    # let's slice it
                    return line[12:-2]
    return 'DETECT'
