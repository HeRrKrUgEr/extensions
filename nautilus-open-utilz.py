# This example is contributed by Vincent Chanliau
import os

# A way to get unquote working with python 2 and 3
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject


class OpenTerminalExtension(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        pass

    def _run_command(self, file, command):
        wd = unquote(file.get_uri()[7:])
        if not file.is_directory():
            print(file.get_parent_location())
            wd = wd.replace(file.get_name(), '')
        os.chdir(wd)
        os.system(command)

    def menu_openTerminal(self, menu, file):
        self._run_command(file, "gnome-terminal")

    def menu_openWithCode(self, menu, file):
        self._run_command(file, "code .")

    def menu_install_deb(self, menu, file):
        self._run_command(
            file, "gnome-terminal -e 'sudo dpkg -i %s' --" % file.get_name())

    def get_file_items(self, window, files):
        return self._create_menu_items(files, "File")

    def get_background_items(self, window, file):
        return self._create_menu_items([file], "Background")

    def _create_menu_items(self, files, group):

        if len(files) != 1:
            return

        file = files[0]

        if file.get_uri_scheme() != 'file':
            return

        itemTerm = Nautilus.MenuItem(
            name='NautilusPython::openterminal' + group,
            label='Open folder in Terminal',
            tip='Open %s in Terminal' % file.get_name())
        itemTerm.connect('activate', self.menu_openTerminal, file)

        itemCode = Nautilus.MenuItem(name='NautilusPython::opencode' + group,
                                     label='Open folder in Code',
                                     tip='Open Folder %s in VSCode' %
                                     file.get_name())
        itemCode.connect('activate', self.menu_openWithCode, file)

        items = [itemTerm, itemCode]

        if not file.is_directory() and not file.get_name()[0] == '.':

            if file.is_mime_type("application/vnd.debian.binary-package"):
                itemDeb = Nautilus.MenuItem(
                    name='NautilusPython::opendeb_file_item',
                    label='Instal package',
                    tip='Install %s DEB package' % file.get_name())
                itemDeb.connect('activate', self.menu_install_deb, file)
                items.insert(1, itemDeb)
        return items
