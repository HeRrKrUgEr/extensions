import os
from gi.repository import Nautilus, GObject, Gtk, Gdk
from gi import require_version

require_version('Gtk', '3.0')
require_version('Nautilus', '3.0')


class NautilusCopyPath(Nautilus.MenuProvider, GObject.GObject):
    def __init__(self):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def get_file_items(self, window, files):
        return self._create_menu_items(files, "File")

    def get_background_items(self, window, file):
        return self._create_menu_items([file], "Background")

    def _create_menu_items(self, files, group):
        plural = len(files) > 1
        item_path = Nautilus.MenuItem(
            name="NautilusCopyPath::CopyPath" + group,
            label="Copy Paths" if plural else "Copy Path",
        )
        item_name = Nautilus.MenuItem(
            name="NautilusCopyPath::CopyName" + group,
            label="Copy Names" if plural else "Copy Name",
        )

        item_path.connect("activate", self._copy_paths, files)
        item_name.connect("activate", self._copy_names, files)
        return [item_path, item_name]

    def _copy_paths(self, menu, files):
        paths = list(map(lambda f: f.get_location().get_path(), files))
        if len(paths) > 0:
            self.clipboard.set_text(", ".join(paths), -1)

    def _copy_names(self, menu, files):
        paths = list(
            map(lambda x: os.path.basename(x.get_location().get_path()),
                files))
        if len(paths) > 0:
            self.clipboard.set_text(", ".join(paths), -1)
