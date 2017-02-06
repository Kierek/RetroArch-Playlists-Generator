import os
import sys

from modules.generator import fire_generator, find_core_name


class NoGUIResolver:
    starting_directory = None

    def __init__(self, cores_location):
        # ask user for starting directory only first time
        self.cores_location = cores_location
        self.starting_directory = input("Enter your starting directory, with system specific directories: ")

    def set_system(self):
        from playlist_creator import systems_list, default_info_files_location

        directories = sorted(os.listdir(self.starting_directory))

        # print all available systems
        for x in range(len(systems_list)):
            print(x, systems_list[x])

        # ask user to chose system
        system_id = input("Choose system: ")
        picked_system = systems_list[int(system_id)]

        for x in range(len(directories)):
            print(x, directories[x])

        # ask user for folder with ROMS
        roms_dir_id = input("{} ROMS directory: ".format(picked_system))
        roms_dir = os.path.join(self.starting_directory, directories[int(roms_dir_id)])

        all_cores = sorted(os.listdir(self.cores_location))

        for x in range(len(all_cores)):
            print(x, all_cores[x])

        # ask user for core
        core_id = input("Select core for {} system: ".format(picked_system))

        # pick core file
        selected_core = os.path.join(self.cores_location, all_cores[int(core_id)])

        import playlist_creator
        fire_generator(playlist_creator.default_playlists_location, roms_dir, picked_system, selected_core,
                       find_core_name(selected_core, default_info_files_location))
        self.ask_if_done()

    def ask_if_done(self):
        are_we_done = input("Continue? (y/n) ")
        if are_we_done is "y":
            self.set_system()
        else:
            sys.exit(0)
