import sys
import threading, queue
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Resolves error: "attempted relative import with no known parent package"
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
if __name__ == '__main__':
    from interface.settings.Settings import res_dir
    from interface.gui.GuiManager import GuiManager
    from NodeConnector import NodeConnector
else:
    from .interface.settings.Settings import res_dir
    from .interface.gui.GuiManager import GuiManager
    from .NodeConnector import NodeConnector


class ClaverMessageBoard(Gtk.Application):

    BUILD_NUMBER = "Summer 2020 (dev)"
    # https://github.com/zestsoftware/zest.releaser
    # https://pypi.org/project/bumpversion/

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

    def __init__(self, ip_address, port, request_callback=None, launcher_data=None):
        Gtk.Application.__init__(self)

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(res_dir['CSS_MAIN'] + 'style.css')
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.__gui_manager = GuiManager(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.is_fullscreen = False

        self.queue = queue.Queue()
        self.node_connector = NodeConnector(self, self.queue, ip_address, port)
        self.t1 = threading.Thread(target=self.node_connector.run_asyncio)
        self.t1.daemon = True
        self.t1.start()
        self.request_callback = request_callback
        if request_callback is not None:
            self.request_callback(0)
        if launcher_data is not None:
            self.messages_sent({"initialization": launcher_data})

    def do_activate(self):
        """ Initializes the application window """

        window = Gtk.Window(application=self)
        window.set_title("Claver Communication Board")
        window.set_default_size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        window.set_icon_from_file(res_dir['ROOT'] + 'icon.png')
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("size-allocate", self.on_resize)
        window.connect("key-release-event", self.on_key_release)
        window.connect("destroy", self.cleanup)

        # Adds a drawing layer to the window
        window.add(self.__gui_manager.getOverlay())

        window.show_all()

    def on_key_release(self, window, event):
        if event.keyval == Gdk.KEY_Escape:
            self.quit_application()
        elif event.keyval == Gdk.KEY_f or event.keyval == Gdk.KEY_F:
            self.fullscreen_mode(window)

    def cleanup(self, widget):
        print("Closing window")
        self.queue.put("cleanup")
        return False

    def quit_application(self):
        self.queue.put("cleanup")
        self.quit()

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

    def messages_received(self, data):
        """ Reveives message from thread running asyncio websocket """
        if type(data) is dict:
            # Look for actionable directives sent to the GTK app (restart, shutdown, etc)
            if "type" in data and data["type"] == "directive":
                if data["value"] == "restart":
                    self.quit_application()
            else:
                self.__gui_manager.process_message(data)

    def messages_sent(self, message):
        """ Sends message to thread queue for processing by asyncio websocket """
        self.queue.put(message)

if __name__ == "__main__":
    application = ClaverMessageBoard("192.168.1.25", "6789")
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)


""""
Resources: Temperature & CPU of RPi
https://www.raspberrypi.org/forums/viewtopic.php?t=252115
"""