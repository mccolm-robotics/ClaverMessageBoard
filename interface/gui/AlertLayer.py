import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from ..settings.Settings import *


class AlertLayer:
    """ Initializes a GTK layout container for use in a GTK.Overlay. This class is instantiated by the GuiManager. """
    def __init__(self, gui_manager):
        """ Constructor """
        self.__gui_manager = gui_manager
        self.__default_css_class = default_css_class
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)                        # Add a box below the message bar
        self.__layout_container.set_hexpand(True)                                                      # Set box height to 100% of remaining space
        self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class('alert-background')

        self.__contents_being_displayed = None

    def get_layout_container(self):
        """ Public: Returns Gtk layout container """
        return self.__layout_container

    def show_content(self, content):
        """ Public: Add content to the layout container """
        if self.__contents_being_displayed is not None:
            self.clear_content()
        self.__contents_being_displayed = content
        self.__layout_container.add(content)
        self.__layout_container.show_all()

    def clear_content(self):
        """ Public: Remove content from the layout container """
        self.__layout_container.remove(self.__contents_being_displayed)
        self.__contents_being_displayed = None