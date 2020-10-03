import sys
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from interface.settings.Settings import res_dir
from interface.gui.GuiManager import GuiManager
from interface.network.NodeClient import NodeClient

class Claver_Main(Gtk.Application):

    BUILD_NUMBER = "Summer 2020 (dev)"
    # https://github.com/zestsoftware/zest.releaser
    # https://pypi.org/project/bumpversion/

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

    def __init__(self):
        Gtk.Application.__init__(self)

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(res_dir['CSS_MAIN'] + 'style.css')
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.__gui_manager = GuiManager(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.is_fullscreen = False

    def do_activate(self):
        """ Initializes the application window """

        window = Gtk.Window(application=self)
        window.set_title("Claver Communication Board")
        window.set_default_size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        window.set_icon_from_file(res_dir['ROOT'] + 'icon.png')
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("size-allocate", self.on_resize)
        window.connect("key-release-event", self.on_key_release)

        # Adds a drawing layer to the window
        window.add(self.__gui_manager.getOverlay())

        window.show_all()

    def on_key_release(self, window, event):
        if event.keyval == Gdk.KEY_Escape:
            self.quit()
        elif event.keyval == Gdk.KEY_f or event.keyval == Gdk.KEY_F:
            self.fullscreen_mode(window)

    def fullscreen_mode(self, window):
        if self.is_fullscreen == True:
            window.unfullscreen()
            self.is_fullscreen = False
        else:
            window.fullscreen()
            self.is_fullscreen = True

    def on_resize(self, window, size_rect):
        """ Stores the new width and height of window after resized """

        self.WINDOW_WIDTH = size_rect.width
        self.WINDOW_HEIGHT = size_rect.height
        self.__gui_manager.updateContentAreaDimensions(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

if __name__ == "__main__":
    application = Claver_Main()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)