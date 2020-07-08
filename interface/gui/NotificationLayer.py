import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
import interface.settings.Settings as settings

class NotificationLayer:
    def __init__(self):
        """ Constructor """
        self.__default_css_class = settings.default_css_class
        self.__temp_css_class = None
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)  # Create a grid to manage containers
        self.__build_layer()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of notification area """
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)                     # Add a box to contain messages
        top_bar.get_style_context().add_class('message-bar')                          # Connect CSS class to box
        top_bar.set_hexpand(True)                                                     # Set the box to expand 100%
        label = Gtk.Label()                                                                         # Add a label to the box
        label.set_text("Notifications")                                                             # Set the value of the label text
        label.get_style_context().add_class('label-notification')                                   # Connect a CSS class to the label
        top_bar.add(label)                                                            # Add the label into the box

        self.__layout_container.attach(child=top_bar, left=0, top=0, width=1, height=1)  # Attach the box to the layout at 0, 0

        self.__message_layer_bottom = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)                        # Add a box below the message bar
        self.__message_layer_bottom.set_hexpand(True)                                                      # Set box height to 100% of remaining space
        self.__message_layer_bottom.set_vexpand(True)
        self.__message_layer_bottom.get_style_context().add_class(self.__default_css_class)                             # Connect a CSS class to the box (background colour)
        self.__layout_container.attach(child=self.__message_layer_bottom, left=0, top=1, width=1, height=1)   # Attach this box to the layout below the message bar

    def getContentBoxAllocation(self):
        return self.__message_layer_bottom.get_allocation()

    def setBackgroundColour(self, css_class):
        self.__temp_css_class = css_class
        self.__message_layer_bottom.get_style_context().remove_class(self.__default_css_class)
        self.__message_layer_bottom.get_style_context().add_class(css_class)
        self.__message_layer_bottom.show_all()

    def restoreBackgroundColour(self):
        self.__message_layer_bottom.get_style_context().remove_class(self.__temp_css_class)
        self.__message_layer_bottom.get_style_context().add_class(self.__default_css_class)
        self.__message_layer_bottom.show_all()