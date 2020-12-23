import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from .AlertAuthorization import AlertAuthorization
from .AlertNotificationPanel import AlertNotificationPanel
from ..settings.Settings import *


class NotificationManager:
    """ Manages adding and removing notifications from the notifications layer. Instantiated in the gui manager. """
    def __init__(self, gui_manager):
        """ Class constructor """
        self.__gui_manager = gui_manager
        self.__message_builder = gui_manager.get_message_builder()
        self.__notification_container = gui_manager.get_notification_layer_container()     # Gtk.Grid to hold content for the notification area
        self.__notifications_list = []                      # List of all active notifications
        self.__current_notification_widget = None           # Track the currently visible notification widget
        self.__current_notification_id = None               # Track the id (list index) of the current notification
        self.__current_action_button = None                 # Track the currently visible action button
        self.__collapsed_notification_count_label = Gtk.Label() # Label showing the total number of notifications stored in notifications_list (visible on the main screen)
        self.__expanded_notification_count_label = None     # Label showing the total number of notifications stored in the notifications_list (visible only in the notification panel)


        # Notifications label box
        self.label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.label_box.set_hexpand(True)
        self.__notification_container.attach(child=self.label_box, left=0, top=0, width=1, height=1)

        # Add box to contain 'dismiss', 'settings, and 'show all' buttons
        self.notification_action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.__notification_container.attach(child=self.notification_action_box, left=1, top=0, width=1, height=1)

        # Add a button to show the notification panel area
        self.__add_list_button()

    def get_message_builder(self):
        """ Public: Returns the message builder object. Instantiated in the gui manager. """
        return self.__message_builder

    def get_notification_list(self):
        """ Public: Returns the list of current notifications """
        return self.__notifications_list

    def update_notification_count_labels(self, count):
        """ Public: Set the text values on the notification count labels. """
        self.__collapsed_notification_count_label.set_text(str(count))
        if self.__expanded_notification_count_label is not None:
            self.__expanded_notification_count_label.set_text(str(count))

    def add_notification(self, mode_action: dict, notification: str, priority: int = 3, alert_type: str = None):
        """ Public: Add message to list of active notifications """
        # See https://github.com/mccolm-robotics/ClaverMessageBoard/wiki/Message-Structure for information about the message structure
        notification = {'mode_action': mode_action, 'text': notification, 'priority': priority, 'alert': alert_type}    # Build a record of the notification
        self.__notifications_list.append(notification)                  # Store record in a list
        notification_id = len(self.__notifications_list) - 1                                                            # Set notification to list index value
        notification_count = len(self.__notifications_list)
        self.update_notification_count_labels(notification_count)

        # priority: 3 - display in order of receipt; 2 - display at top of list; 1 - display as blocking alert
        if self.__current_notification_widget is None or notification["priority"] == 2:
            if self.__current_notification_widget is not None:  # Check to see if a notification widget is currently showing
                self.label_box.remove(self.__current_notification_widget)   # Remove current notification from box
                if self.__current_action_button is not None:
                    self.notification_action_box.remove(self.__current_action_button)
                    self.__current_action_button = None
            self.__current_notification_widget = self.add_notification_action(notification=notification, callback=self.__on_notification_pressed, id=len(self.__notifications_list) - 1)
            self.__current_notification_id = notification_id
            self.label_box.add(self.__current_notification_widget)   # Add Gtk.EventBox for new notification
            self.label_box.show_all()   # Display notification in the display box
        if notification["priority"] > 1:    # Add appropriate action buttons for the notification type
            if notification["mode_action"]["target"] == "settings":
                self.__add_settings_button(notification_id)
            else:
                self.__add_dismiss_button()

    def get_current_notification_id(self):
        return self.__current_notification_id

    def add_notification_action(self, notification: dict, callback: classmethod, id: int) -> Gtk.Widget:
        """ Public: Creates a GtkEventBox and Label for each notification """
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
        notification_action.connect('button-press-event', callback)     # Connect to click event.
        notification_action.set_can_focus(False)    # Prevent widget focus
        notification_action.set_name(str(id))      # This name will be used to identify the notification and specific action
        return notification_action      # Return this widget to calling function

    def __on_notification_pressed(self, widget, event):
        """ Private: Callback function for the notification clicked event """
        if 'GDK_BUTTON_PRESS' in str(event.type):  # If the user made a "single click"
            if event.button == Gdk.BUTTON_PRIMARY:  # If it is a left click
                notification_id = int(widget.get_name())
                print("Taking notification action...")
                
    def __create_button(self, image: str, callback: classmethod, width: int = 40, height: int = 40, css_class: str = 'notification-button', label: Gtk.Label = None, id: int = None) -> Gtk.Widget:
        """ Creates a GTK.Button with image from png. Button clicks are connected to 'callback' and an optional label is added from 'label'. """
        # Perform check to make sure png file is valid?
        formatting_box = Gtk.Box()
        formatting_box.get_style_context().add_class(css_class)     # Add CSS class 'notification-button' to style button -> adds left margin spacing
        action_button = Gtk.EventBox()                                           # Create new Gtk.Button
        formatting_box.add(action_button)
        action_button.set_can_focus(False)                                     # Keep the button from holding focus. This is a touch-screen and the focus indicator shows as a dotted line around button
        action_button.connect("button-press-event", callback)            # Add dedicated action callback function to button
        if id is not None:
            action_button.set_name(str(id))
        if label is not None:
            preserve_ratio = False
        else:
            preserve_ratio = True
        image_buffer = GdkPixbuf.Pixbuf.new_from_file_at_scale(        # Create a pixel buffer to hold button image. This buffer is filled with the data from a png image.
            filename=res_dir['BUTTON_IMAGES'] + image,           # The directory path for the resource folder is stored in a dictionary in a settings file
            width=width,
            height=height,
            preserve_aspect_ratio=preserve_ratio)
        image_pb = Gtk.Image.new_from_pixbuf(image_buffer)             # Create a Gtk.Image from the data stored in the Gdk Pixel Buffer
        if label is not None:
            grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
            grid.attach(image_pb, 0, 0, 1, 1)
            grid.attach(label, 0, 1, 1, 1)
            action_button.add(grid)
        else:
            action_button.add(image_pb)
        return formatting_box

    def create_dismiss_button(self, callback: classmethod, width: int = 40, height: int = 40, css_class: str = "notification-button", id: int = None):
        """ Public: Create a new 'dismiss' button that displays the 'delete' image """
        return self.__create_button(image="button_delete.png", callback=callback, width=width, height=height, css_class=css_class, id=id)

    def create_list_button(self, callback: classmethod):
        """ Public: Create a new 'list' button that displays the 'arrow_expand' image """
        return self.__create_button(image="arrow_expand.png", callback=callback, width=40, height=30, label=self.__collapsed_notification_count_label)
    
    def create_collapse_list_button(self, callback: classmethod):
        """ Public: Create a new button showing the 'collapse' image and the current number of notifications """
        self.__expanded_notification_count_label = Gtk.Label(str(len(self.__notifications_list)))   # A new label is created because GTK does not allow the same widget to be attached more than once simultaneously. Python automatically garbage collects the last label.
        return self.__create_button(image="arrow_collapse.png", callback=callback, width=40, height=30, label=self.__expanded_notification_count_label)

    def create_settings_button(self, callback: classmethod, id: int = None):
        """ Public: Create a new button showing the 'settings' image """
        return self.__create_button(image="button_settings.png", callback=callback, id=id)

    def create_generic_button(self, image: str, callback: classmethod, width: int, height: int, css_class: str, label: Gtk.Label = None):
        """ Public: General button creation interface """
        return self.__create_button(image=image, callback=callback, width=width, height=height, css_class=css_class, label=label)


    def __add_dismiss_button(self):
        """ Private: Add dismiss action button to notification action box. """
        self.__current_action_button = self.create_dismiss_button(self.__on_dismiss_clicked)
        self.notification_action_box.pack_start(self.__current_action_button, False, False, 0)                        # Add button to the notification action-area box
        self.notification_action_box.show_all()

    def __on_dismiss_clicked(self, button):
        """ Private: Callback function for the 'dismiss' button """
        test_alert = AlertAuthorization(self.__gui_manager)
        self.__gui_manager.show_alert(test_alert.get_content())

    def __add_list_button(self):
        """ Private: Add list action button to notification action box. """
        list_button = self.create_list_button(self.__on_list_clicked)
        self.notification_action_box.pack_end(list_button, False, False, 0)
        self.notification_action_box.show_all()

    def __on_list_clicked(self, widget, event):
        """ Private: Callback function for the 'list' button """
        notification_panel = AlertNotificationPanel(self.__gui_manager)
        self.__gui_manager.show_alert(notification_panel.get_content())

    def __add_settings_button(self, id: int):
        """ Private: Add settings action button to notification action box. """
        # Add 'show_all' button to notification action box
        self.__current_action_button = self.create_settings_button(callback=self.__on_settings_clicked, id=id)
        self.notification_action_box.pack_end(self.__current_action_button, False, False, 0)
        self.notification_action_box.show_all()

    def __on_settings_clicked(self, widget, event):
        """ Private: Callback function for the 'settings' button """
        if self.__notifications_list[int(widget.get_name())]["mode_action"]["action"] == "display_menu":
            self.__gui_manager.load_content_area(menu_labels[8][0], self.__notifications_list[int(widget.get_name())]["mode_action"]["values"]["menu"])