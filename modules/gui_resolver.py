import json
import os
import gi

from modules import generator

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from modules.generator import fire_generator


class GUIResolver:
    systems = []

    def __init__(self):
        from playlist_creator import preferences_file_location, systems_list

        self.settings_file_location = preferences_file_location
        with open(self.settings_file_location) as data_file:
            self.preferences_data = json.load(data_file)

        builder = Gtk.Builder()
        builder.add_from_file("glade/app.glade")
        builder.connect_signals(self)

        self.notebook = builder.get_object("notebook")
        self.renderer_text = Gtk.CellRendererText()

        self.playlists_directory_chooser = builder.get_object("playlists_directory_chooser")
        self.cores_directory_chooser = builder.get_object("cores_directory_chooser")
        self.infos_directory_chooser = builder.get_object("infos_directory_chooser")

        self.playlists_location = self.preferences_data[0]['playlists_location']
        self.cores_location = self.preferences_data[0]['cores_location']
        self.infos_location = self.preferences_data[0]['infos_location']

        self.playlists_directory_chooser.set_current_folder(self.playlists_location)
        self.cores_directory_chooser.set_current_folder(self.cores_location)
        self.infos_directory_chooser.set_current_folder(self.infos_location)

        self.system_names = Gtk.ListStore(str)
        for system_name in systems_list:
            self.system_names.append([system_name])

        # get all cores and populate list
        self.__populate_cores_list__()

        if len(self.preferences_data) > 1:
            for system_from_prefs in self.preferences_data[1]:
                self.create_new_tab(system_from_prefs['system_name'], system_from_prefs['roms_dir'],
                                    system_from_prefs['core_path'], system_from_prefs['core_name'])

        window = builder.get_object("window")
        window.show_all()
        Gtk.main()

    def __populate_cores_list__(self):
        self.cores_list = Gtk.ListStore(str)
        for core in sorted(os.listdir(self.cores_location)):
            self.cores_list.append([core])

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

    def playlists_directory_changed(self, widget):
        self.playlists_location = widget.get_file().get_path()

    def cores_directory_changed(self, widget):
        self.cores_location = widget.get_file().get_path()
        self.__populate_cores_list__()

    def infos_directory_changed(self, widget):
        self.infos_location = widget.get_file().get_path()

    def generate_clicked(self, *args):
        for system_generator in self.systems:
            fire_generator(self.playlists_location, system_generator.roms_dir,
                           system_generator.system_name,
                           system_generator.core_path, system_generator.core_name)

    def save_profile_clicked(self, widget):
        config = {'playlists_location': self.playlists_location,
                  'cores_location': self.cores_location,
                  'infos_location': self.infos_location}

        system_configs = []

        for system_page in self.systems:
            system_config = {'system_name': system_page.system_name,
                             'roms_dir': system_page.roms_dir,
                             'core_path': system_page.core_path,
                             'core_name': system_page.core_name}
            system_configs.append(system_config)

        with open(self.settings_file_location, 'w') as f:
            json.dump([config, system_configs], f, indent=4)

    def new_tab_clicked(self, *args):
        self.create_new_tab()

    def create_new_tab(self, system_name=None, roms_dir=None, core_path=None, core_name=None):
        notebook_id = self.notebook.get_n_pages()

        builder = Gtk.Builder()
        builder.add_from_file("glade/system_tab.glade")

        core_name_label = builder.get_object("detected_name_label")

        new_system_generator = SystemGenerator(self, core_name_label, system_name,
                                               roms_dir, core_path, core_name)

        builder.connect_signals(new_system_generator)

        new_page = builder.get_object("system_box")

        self.notebook.append_page(new_page, Gtk.Label('System: {}'.format(notebook_id)))
        self.notebook.show_all()

        system_combobox_placeholder = builder.get_object("system_combobox")
        core_combobox_placeholder = builder.get_object("core_combobox")

        system_combobox = Gtk.ComboBox.new_with_model(self.system_names)
        system_combobox.connect("changed", new_system_generator.change_system_name)
        system_combobox.pack_start(self.renderer_text, True)
        system_combobox.add_attribute(self.renderer_text, "text", 0)
        system_combobox_placeholder.pack_start(system_combobox, False, False, True)

        system_combobox.show_all()

        core_combobox = Gtk.ComboBox.new_with_model(self.cores_list)
        core_combobox.connect("changed", new_system_generator.core_changed)
        core_combobox.pack_start(self.renderer_text, True)
        core_combobox.add_attribute(self.renderer_text, "text", 0)
        core_combobox_placeholder.pack_start(core_combobox, False, False, True)

        core_combobox.show_all()

        if core_path is not None:
            core_combobox.set_active(self.get_core_index(os.path.basename(core_path)))

        if system_name is not None:
            system_combobox.set_active(self.get_system_index(system_name))

        if roms_dir is not None:
            roms_dir_file_choose = builder.get_object("roms_directory_chooser")
            roms_dir_file_choose.set_current_folder(roms_dir)

        self.systems.append(new_system_generator)

    def get_system_index(self, system_name):
        i = 0
        import playlist_creator
        for system in playlist_creator.systems_list:
            if system == system_name:
                return i
            i += 1

        return 0

    def get_core_index(self, core_file_name):
        i = 0
        for core in sorted(os.listdir(self.cores_location)):
            if core == core_file_name:
                return i
            i += 1
        return 0


class SystemGenerator:
    def __init__(self, resolver_object, core_name_label, system_name,
                 roms_dir, core_path, core_name):
        self.system_name = system_name
        self.roms_dir = roms_dir
        self.core_path = core_path
        self.core_name = core_name
        self.resolver_object = resolver_object
        self.core_name_label = core_name_label

    def change_system_name(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.system_name = model[tree_iter][0]

    def roms_dir_changed(self, widget):
        self.roms_dir = widget.get_file().get_path()

    def core_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.core_path = os.path.join(self.resolver_object.cores_location, model[tree_iter][0])
            self.__change_core_name__(generator.find_core_name(self.core_path,
                                                               self.resolver_object.infos_location))

    def __change_core_name__(self, core_name):
        self.core_name = core_name
        self.core_name_label.set_text(core_name)

    def remove_system_clicked(self, widget):
        # check which page's remove button was clicked
        i = 0
        for system_generator in self.resolver_object.systems:
            if system_generator == self:
                break
            i += 1

        # tab id is equal to first page + systems page, remove it from notebook and system from array
        self.resolver_object.notebook.remove_page(i + 1)
        self.resolver_object.systems.pop(i)
