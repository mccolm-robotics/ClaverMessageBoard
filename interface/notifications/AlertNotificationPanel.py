import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from ..settings.Settings import *


class AlertNotificationPanel:
    """ Displays a list of notifications registered by the NotificationManager. This class is instantiated by the
     NotificationManager and is triggered bo the 'list' button in the notification panel. """

    def __init__(self, gui_manager):
        """ Constructor """
        self.__gui_manager = gui_manager
        self.__notification_manager = gui_manager.get_notification_manager()
        self.__notifications_list = self.__notification_manager.get_notification_list()
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
        notifications_box = Gtk.Box()
        notifications_box.get_style_context().add_class('notification-panel-top')
        notifications_box.set_hexpand(True)
        self.__layout_container.add(notifications_box)

        notifications_grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        notifications_box.add(notifications_grid)

        self.notification_text_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.notification_text_container.set_hexpand(True)

        notifications_grid.attach(child=self.notification_text_container, left=0, top=0, width=1, height=1)

        self.action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.action_box.get_style_context().add_class('notification-panel-top-action')
        notifications_grid.attach(child=self.action_box, left=1, top=0, width=1, height=1)
        self.__add_list_button()

        self.display_notification(notification=self.__notifications_list[-1], primary=True)
        for count in range(len(self.__notifications_list) - 1):
            self.display_notification(notification=self.__notifications_list[count])

    def display_notification(self, notification, primary: bool = False):
        notification_eventbox = self.__notification_manager.add_notification_action(notification, self.__on_event_clicked)
        if primary is True:
            self.notification_text_container.add(notification_eventbox)
            if self.__notifications_list[-1]["priority"] > 1:    # Add appropriate action buttons for the notification type
                if self.__notifications_list[-1]["mode_action"]["target"] == "settings":
                    self.__add_settings_button(self.action_box)
                else:
                    self.__add_dismiss_button(self.action_box)
        else:
            self.__layout_container.add(notification_eventbox)

    def __on_event_clicked(self, event_box, event_button):
        print("Notification Event Clicked")

    def __add_list_button(self):
        # Add 'show_all' button to notification action box
        list_button = self.__notification_manager.create_collapse_list_button(self.__on_list_clicked)    # Allow Notification Manager to create button widget but register local callback for button click
        self.action_box.pack_end(list_button, False, False, 0)
        self.action_box.show_all()

    def __on_list_clicked(self, button):
        self.__gui_manager.close_alert()

    def __add_settings_button(self, layout_container):
        """ Private: Add settings action button to notification action box. """
        # Add 'show_all' button to notification action box
        settings_button = self.__notification_manager.create_settings_button(self.__on_settings_clicked)
        layout_container.pack_start(settings_button, False, False, 0)
        layout_container.show_all()

    def __on_settings_clicked(self, button):
        """ Private: Callback function for the 'settings' button """
        print("Settings Button Clicked")

    def __add_dismiss_button(self, layout_container):
        """ Private: Add dismiss action button to notification action box. """
        action_button = self.__notification_manager.create_dismiss_button(self.__on_dismiss_clicked)
        layout_container.pack_start(action_button, False, False, 0)
        layout_container.show_all()

    def __on_dismiss_clicked(self, button):
        """ Private: Callback function for the 'dismiss' button """
        print("Dismiss Button Clicked")