import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from ..settings.Settings import *


class AlertNotificationPanel:
    """ Displays a list of notifications registered by the NotificationManager. This class is instantiated by the
    NotificationManager and is triggered by the 'list' button in the notification panel. Click-through is disabled
    since the main overlay container obscures the layers below it. """

    def __init__(self, gui_manager):
        """ Constructor """
        self.__gui_manager = gui_manager
        self.__notification_manager = gui_manager.get_notification_manager()
        self.__notifications_list = self.__notification_manager.get_notification_list()
        self.__notification_widget_list = {}
        self.__build_layer()

    def get_content(self):
        """ Public: Returns a GTK.Layout object """
        return self.__page_layout_container

    def __build_layer(self):
        """ Initilization: composes layout of alert area """
        # A box to hold the notifications list
        self.__page_layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__page_layout_container.get_style_context().add_class('notification-panel')  # Connect a CSS class to the box. Adds left & right margins
        self.__page_layout_container.set_hexpand(True)   # Expand horizontally
        self.__page_layout_container.set_vexpand(True)   # Expand vertically

        # A box to hold the primary (top) notification
        primary_notification_box = Gtk.Box()
        primary_notification_box.get_style_context().add_class('notification-panel-top')    # Sets bg colour and height
        primary_notification_box.set_hexpand(True)      # Expand horizontally
        self.__page_layout_container.add(primary_notification_box)   # Add to the primary notification area

        # Adds layout grid to the primary notification box
        notifications_grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        primary_notification_box.add(notifications_grid)

        # Adds a box to hold the primary notification text label
        self.notification_text_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.notification_text_container.set_hexpand(True)
        notifications_grid.attach(child=self.notification_text_container, left=0, top=0, width=1, height=1)

        # Adds a box to the primary notification area to hold action buttons
        self.action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.action_box.get_style_context().add_class('notification-panel-top-action')
        notifications_grid.attach(child=self.action_box, left=1, top=0, width=1, height=1)
        self.__add_list_button()

        # Adds a box to display other notifications not shown in the top bar area
        self.notification_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.notification_panel.get_style_context().add_class('notification-panel-bg')
        self.notification_panel.set_vexpand(True)
        self.__page_layout_container.add(self.notification_panel)

        # Adds a box to display power button and settings option button
        self.notifications_panel_footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.notifications_panel_footer.set_hexpand(True)
        self.notifications_panel_footer.get_style_context().add_class('notification-panel-footer')
        self.notifications_panel_footer.add(self.__panel_footer_contents())
        self.__page_layout_container.add(self.notifications_panel_footer)

        # Display all notifications registered in __notifications_list
        notification_count = len(self.__notifications_list)
        primary_notification_id = self.__notification_manager.get_current_notification_id() # Get id of primary (displayed in top bar) notification
        for count in range(notification_count):
            if count != primary_notification_id:
                self.display_notification(notification=self.__notifications_list[count], id=count)
            else:
                self.display_notification(notification=self.__notifications_list[primary_notification_id], id=primary_notification_id, primary=True)  # Display in top bar

    def display_notification(self, notification: dict, id: int, primary: bool = False):
        notification_eventbox = self.__notification_manager.add_notification_action(notification=notification, callback=self.__on_event_clicked, id=id)
        if primary is True:
            self.notification_text_container.add(notification_eventbox)
            if notification["priority"] > 1:    # Add appropriate action buttons for the notification type
                if notification["mode_action"]["target"] == "settings":
                    self.__add_settings_button(layout_container=self.action_box, id=id)
                else:
                    self.__add_dismiss_button(layout_container=self.action_box, id=id, primary=True)
        else:
            self.__notification_widget_list[str(id)] = self.__package_notification(notification=notification, id=id)
            self.notification_panel.add(self.__notification_widget_list[str(id)])

    def __package_notification(self, notification: dict, id: int):
        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        container.add(action_area)
        self.__add_dismiss_button(action_area, id=id, primary=False)
        text_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        text_area.set_hexpand(True)
        container.add(text_area)
        notification_eventbox = self.__notification_manager.add_notification_action(notification=notification, callback=self.__on_event_clicked, id=id)
        text_area.add(notification_eventbox)
        return container

    def __package_panel_setting(self, text: str, callback: classmethod):
        formatting_container = Gtk.Box()
        clickable_setting = Gtk.EventBox()
        formatting_container.add(clickable_setting)
        clickable_setting.connect('button-press-event', callback)
        label = Gtk.Label()
        label.set_text(text)
        label.get_style_context().add_class('notification-panel-setting-label')
        clickable_setting.add(label)
        return formatting_container

    def __panel_footer_contents(self) -> Gtk.Widget:
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        footer_box.get_style_context().add_class('notification_panel-footer-box')
        footer_box.set_hexpand(True)
        power_button = self.__notification_manager.create_generic_button(image="power_button.png", callback=self.__on_power_clicked, width=25, height=25, css_class="notification-button-panel")
        footer_box.pack_end(power_button, False, False, 0)
        notifications_settings = self.__package_panel_setting("Notification Settings", self.__on_notifications_settings_clicked)
        footer_box.pack_end(notifications_settings, False, False, 0)
        time_label = Gtk.Label()
        time_label.set_text("Mon Dec 21 11:12 PM")
        time_label.get_style_context().add_class('notification-panel-setting-label')
        footer_box.add(time_label)
        network_button = self.__notification_manager.create_generic_button(image="network.png", callback=self.__on_network_settings_clicked, width=20, height=20, css_class="notification-button-panel-icon")
        footer_box.add(network_button)
        volume = Gtk.VolumeButton(size=Gtk.IconSize.LARGE_TOOLBAR, orientation=Gtk.Orientation.VERTICAL)
        volume.set_value(0.8)
        volume.connect('value-changed', self.__on_volume_changed)
        footer_box.add(volume)
        return footer_box

    def __on_volume_changed(self, widget, level):
        print(f"Volume changed {round(level, 1)}")

    def __on_sound_settings_clicked(self, widget, event):
        print("Sound Notifications clicked")

    def __on_network_settings_clicked(self, widget, event):
        self.__gui_manager.close_alert_layer()
        self.__gui_manager.load_content_area(menu_labels[8][0], "Network")

    def __on_notifications_settings_clicked(self, widget, event):
        print("Notifications Settings clicked")

    def __on_power_clicked(self, widget, event):
        self.__gui_manager.quit_program()

    def __on_event_clicked(self, widget, event):
        print("Event button clicked")

    def __add_list_button(self):
        # Add 'show_all' button to notification action box
        list_button = self.__notification_manager.create_collapse_list_button(self.__on_list_clicked)    # Allow Notification Manager to create button widget but register local callback for button click
        self.action_box.pack_end(list_button, False, False, 0)
        self.action_box.show_all()

    def __on_list_clicked(self, widget, event):
        self.__gui_manager.close_alert_layer()

    def __add_settings_button(self, layout_container, id: int):
        """ Private: Add settings action button to notification action box. """
        # Add 'show_all' button to notification action box
        settings_button = self.__notification_manager.create_settings_button(callback=self.__on_settings_clicked, id=id)
        layout_container.pack_start(settings_button, False, False, 0)
        layout_container.show_all()

    def __on_settings_clicked(self, widget, event):
        """ Private: Callback function for the 'settings' button """
        if self.__notifications_list[int(widget.get_name())]["mode_action"]["action"] == "display_menu":
            self.__gui_manager.close_alert_layer()
            self.__gui_manager.load_content_area(menu_labels[8][0], self.__notifications_list[int(widget.get_name())]["mode_action"]["values"]["menu"])

    def __add_dismiss_button(self, layout_container, id: int, primary: bool = False):
        """ Private: Add dismiss action button to notification action box. """
        if primary is False:
            dismiss_button = self.__notification_manager.create_dismiss_button(callback=self.__on_dismiss_clicked, width=20, height=20, css_class="notification-panel-button-circle", id=id)
        else:
            dismiss_button = self.__notification_manager.create_dismiss_button(callback=self.__on_dismiss_clicked, id=id)
        layout_container.pack_start(dismiss_button, False, False, 0)
        layout_container.show_all()

    def __on_dismiss_clicked(self, widget, event):
        """ Private: Callback function for the 'dismiss' button """
        print(f"Dismiss Button Clicked {widget.get_name()}")
        # Remove widget (using GTK object id stored in __notification_widget_list as its name) from notification_panel.
        # Widget is stored in a dict with index set to int (corresponds to index of notification from __notifications_list
        self.notification_panel.remove(self.__notification_widget_list[widget.get_name()])
        del self.__notifications_list[int(widget.get_name())]
        self.__notification_manager.update_notification_count_labels(count=len(self.__notifications_list))
