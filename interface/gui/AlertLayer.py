import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from ..settings.Settings import *


class AlertLayer:
    def __init__(self):
        """ Constructor """
        self.__default_css_class = default_css_class
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of menu area """

        content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # content_area.set_hexpand(True)
        # content_area.set_vexpand(True)
        content_area.get_style_context().add_class(self.__default_css_class)

        notification_label = Gtk.Label()  # Create a new label
        notification_label.set_text("This is an alert")  # Set the value of the label text
        # notification_label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        # notification_label.set_hexpand(True)
        # notification_label.set_vexpand(True)

        content_area.add(notification_label)

        self.__layout_container.attach(child=content_area, left=0, top=0, width=1, height=1)

    def getContentBoxAllocation(self):
        return self.__content_area.get_allocation()