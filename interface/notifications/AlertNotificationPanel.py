import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AlertNotificationPanel:
    """ Displays a list of notifications registered by the NotificationManager. This class is instantiated by the
     NotificationManager and is triggered bo the 'list' button in the notification panel. """

    def __init__(self, gui_manager):
        """ Constructor """
        self.__gui_manager = gui_manager
        self.__build_layer()

    def get_content(self):
        """ Public: Returns a GTK.Layout object """
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of alert area """
        # A smaller box. Size set in CSS. Centered in background box
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__layout_container.get_style_context().add_class('notification-panel')  # Connect a CSS class to the box
        self.__layout_container.set_hexpand(True)
        self.__layout_container.set_vexpand(True)

        # self.__layout_container.set_halign(Gtk.Align.CENTER)
        # self.__layout_container.set_valign(Gtk.Align.CENTER)