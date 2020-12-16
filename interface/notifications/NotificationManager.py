import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from .AlertAuthorization import AlertAuthorization
from ..settings.Settings import *


class NotificationManager:
    def __init__(self, gui_manager):
        """ Class constructor """
        self.__gui_manager = gui_manager
        self.__notification_container = gui_manager.get_notification_layer_container()     # Gtk.Grid to hold content for the notification area
        self.__notifications_list = []                      # List of all active notifications

        # Notifications label box
        self.label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.label_box.set_hexpand(True)
        self.__notification_container.attach(child=self.label_box, left=0, top=0, width=1, height=1)

        # Add box to contain 'dismiss' and 'show all' buttons
        self.notification_action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.__notification_container.attach(child=self.notification_action_box, left=1, top=0, width=1, height=1)


    def add_notification(self, mode: str, notification: str, priority: int = 3, alert_type: str = None):
        """ Public: Add message to list of active notifications """
        # Message structure
        # message = {'mode': 'system', 'text': '', 'priority': '', 'alert': None, 'display_alert': bool}
        # mode: the object to handle any notification action
        # text: string to display in the notification panel
        # priority: 3 - display in order of receipt; 2 - display at top of list; 1 - display as blocking alert
        # alert: the type of alert to display
        message = {'mode': mode, 'text': notification, 'priority': priority, 'alert': alert_type}   # Build a record of the notification
        self.__notifications_list.append(message)                                                   # Store record in a list
        notification_id = len(self.__notifications_list) - 1                                        # Set notification to list index value
        message = Gtk.Label()
        message.set_text("Hello World")
        self.notification_action_box.add(message)
        self.notification_action_box.show_all()
        button = Gtk.Button()
        button.connect("clicked", self.__on_list_clicked)
        self.label_box.add(button)
        self.label_box.show_all()
        # self.__display_notification(notification_id)                                                # Display notification in GUI

    def __display_notification(self, notification_id: int):
        notification = self.__notifications_list[notification_id]
        num_of_notifications = len(self.__notifications_list)
        # priority: 3 - display in order of receipt; 2 - display at top of list; 1 - display as blocking alert
        if num_of_notifications == 1 or notification["priority"] == 2:
            # What if a level 2 priority is already showing?
            # What if another message already showing? Remove it?
            self.label_box.add(self.__add_notification_action(notification_id))
            self.label_box.show_all()
        if notification["priority"] < 3:
            self.__add_dismiss_button()
        if num_of_notifications > 1:
            self.__add_list_button()

    def __add_notification_action(self, notification_id: int):
        """ Creates a GtkEventBox and Label for each notification """
        notification = self.__notifications_list[notification_id]
        # Add label to event box
        notification_message = Gtk.Label()
        if notification['priority'] == 2:
            notification_message.get_style_context().add_class('label-notification-message-urgent')
        elif notification['priority'] == 3:
            notification_message.get_style_context().add_class('label-notification-message-normal')
        notification_message.set_text(notification['text'])
        # Create event box to capture click events on notification item.
        notification_action = Gtk.EventBox()
        notification_action.add(notification_message)   # Add label from above
        notification_action.connect('button-press-event', self.__on_notification_pressed)     # Connect to click event.
        notification_action.set_can_focus(False)    # Prevent widget focus
        notification_action.set_name(str(notification_id))      # This name will be used to identify the notification and specific action
        return notification_action      # Return this widget to calling function

    def __on_notification_pressed(self, widget, event):
        if 'GDK_BUTTON_PRESS' in str(event.type):  # If the user made a "single click"
            if event.button == Gdk.BUTTON_PRIMARY:  # If it is a left click
                notification_id = int(widget.get_name())
                print("Taking notification action...")

    def __add_dismiss_button(self):
        """ Public: Add action button to notification action box. """
        self.action_button = Gtk.Button()                                           # Create new Gtk.Button
        self.action_button.get_style_context().add_class('notification-button')     # Add CSS class 'notification-button' to style button -> adds left margin spacing
        self.action_button.set_can_focus(False)                                     # Keep the button from holding focus. This is a touch-screen and the focus indicator shows as a dotted line around button
        self.action_button.connect("clicked", self.__on_dismiss_clicked)                # Add dedicated action callback function to button
        dismiss_image_buffer = GdkPixbuf.Pixbuf.new_from_file_at_scale(             # Create a pixel buffer to hold button image. This buffer is filled with the data from a png image.
            filename=res_dir['BUTTON_IMAGES'] + "button_delete.png",                # The directory path for the resource folder is stored in a dictionary in a settings file
            width=40,
            height=40,
            preserve_aspect_ratio=True)
        dismiss_image = Gtk.Image.new_from_pixbuf(dismiss_image_buffer)             # Create a Gtk.Image from the data stored in the Gdk Pixel Buffer
        self.action_button.add(dismiss_image)                                       # Add image to the button
        self.notification_action_box.add(self.action_button)                        # Add button to the notification action-area box
        self.action_button.show_all()

    def __on_dismiss_clicked(self, button):
        test_alert = AlertAuthorization(self.__gui_manager)
        self.__gui_manager.show_alert(test_alert.get_content())

    def __add_list_button(self):
        # Add 'show_all' button to notification action box
        self.__list_button = Gtk.Button()
        self.__list_button.get_style_context().add_class('notification-button')
        self.__list_button.set_can_focus(False)
        self.__list_button.connect("clicked", self.__on_list_clicked)
        show_all_image_buffer = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=res_dir['BUTTON_IMAGES'] + "arrow_drop_down.png",
            width=40,
            height=40,
            preserve_aspect_ratio=True)
        show_all_image = Gtk.Image.new_from_pixbuf(show_all_image_buffer)
        self.__list_button.add(show_all_image)
        self.notification_action_box.add(self.__list_button)
        self.__list_button.show_all()

    def test_button(self):
        button = Gtk.Button()
        button.connect("clicked", self.__on_list_clicked)
        self.notification_action_box.add(button)

    def __on_list_clicked(self, button):
        test_alert = AlertAuthorization(self.__gui_manager)
        self.__gui_manager.show_alert(test_alert.get_content())
