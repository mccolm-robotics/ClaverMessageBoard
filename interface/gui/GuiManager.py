import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .AlertLayer import AlertLayer
from .ContentLayer import ContentLayer
from .MenuLayer import MenuLayer
from .MessageBuilder import MessageBuilder
from .NotificationLayer import NotificationLayer
from ..calendar.CalendarManager import CalendarManager
from ..doodle.DoodleManager import DoodleManager
from ..games.GamesManager import GamesManager
from ..lists.ListsManager import ListsManager
from ..messages.MessagesManager import MessagesManager
from ..news.NewsManager import NewsManager
from ..photos.PhotosManager import PhotosManager
from ..settings.Settings import *
from ..settings.SettingsManager import SettingsManager
from ..system.Router import Router
from ..timer.TimerManager import TimerManager
from ..notifications.NotificationManager import NotificationManager



class GuiManager:

    def __init__(self, window_width, window_height, outbound_message_queue):
        """ Constructor """
        self.__window_width = window_width
        self.__window_height = window_height
        self.__message_builder = MessageBuilder()
        self.__notification_layer = NotificationLayer()
        self.__notification_manager = NotificationManager(self)
        self.__outbound_msg_queue = outbound_message_queue
        self.__interface_layer = Gtk.Overlay()
        self.__layers = []
        self.__updateCallbacks = []
        self.__contentAreaDimensions = [1, 1]
        self.__apps_dict = {
            # This is probably a bad idea if the labels are created using a different character set
            menu_labels[0][0].lower(): DoodleManager(notification_manager=self.__notification_manager),
            menu_labels[1][0].lower(): GamesManager(notification_manager=self.__notification_manager),
            menu_labels[2][0].lower(): MessagesManager(notification_manager=self.__notification_manager),
            menu_labels[3][0].lower(): PhotosManager(notification_manager=self.__notification_manager),
            menu_labels[4][0].lower(): NewsManager(notification_manager=self.__notification_manager),
            menu_labels[5][0].lower(): TimerManager(notification_manager=self.__notification_manager),
            menu_labels[6][0].lower(): CalendarManager(notification_manager=self.__notification_manager),
            menu_labels[7][0].lower(): ListsManager(notification_manager=self.__notification_manager),
            menu_labels[8][0].lower(): SettingsManager(self, notification_manager=self.__notification_manager)
        }
        self.__router = Router(outbound_message_queue=self.__outbound_msg_queue, notification_manager=self.__notification_manager, mode_objects=self.__apps_dict)
        self.__alert_layer = AlertLayer(self)
        self.__activeMenu = None
        self.__build_default_interface()

        #test
        self.__notification_manager.add_notification(mode_action={'test': 'this'}, notification="Hello World", priority=1)

    def get_notification_manager(self):
        """ Public: Returns the notification manager object """
        return self.__notification_manager

    def get_message_builder(self):
        """ Public: Returns the message builder object """
        return self.__message_builder

    def get_router(self):
        """ Public: Returns the router object """
        return self.__router

    def get_notification_layer_container(self):
        """ Public: Returns object reference to Gtk.Widget layout container of the notification layer  """
        return self.__notification_layer.get_notification_container()

    def show_alert(self, content):
        """ Public: Send Gtk.Widget to alert layer for display """
        self.__alert_layer.show_content(content)    # Pass Gtk.Widget (layout container) to alert_layer to be added to Gtk.Overlay
        self.show_alert_layer()     # Move alert_layer to top of Gtk.Overlay stack

    def close_alert(self):
        """ Public: Hides alert layer (Re-orders Gtk.Overlay @ index 3) """
        self.hide_alert_layer()
        self.__alert_layer.clear_content()

    def registerUpdateCallback(self, function):
        """ Callback registration: used by category pages to receive updates about window resize events """
        self.__updateCallbacks.append(function)

    def updateContentAreaDimensions(self, width, height):
        """ Callback function triggered by window resize. Called by Claver __main__.on_resize() """
        self.__window_width = width
        self.__window_height = height
        self.__contentAreaDimensions[0] = self.__layers[1][0].getContentBoxAllocation().width
        self.__contentAreaDimensions[1] = self.__layers[0][0].getContentBoxAllocation().height
        self.__layers[2][0].updateContentAreaDimensions(width, height)

        for function in self.__updateCallbacks:
            function(self.__contentAreaDimensions)

    def setBackgroundColour(self, css_class):
        """ Changes the background colour by setting the overlay widget's container to a different CSS class. """
        self.__layers[0][0].setBackgroundColour(css_class)

    def load_content_area(self, menuItemLabel):
        """ Public: This function swaps out layout containers in the content layer depending on the value of the active
        menu. The value of the menuItemLabel parameter is taken from the label of the menu button that was pressed. """
        if self.__activeMenu is None:
            self.__activeMenu = menuItemLabel
        else:
            self.__layers[2][0].removeLayoutContainer(self.__apps_dict[self.__activeMenu.lower()].getLayoutContainer())
            self.__activeMenu = menuItemLabel
            self.setBackgroundColour(settings_menu_background_classes_dict[menuItemLabel])
        #   Note: __layers[2][0] contains the Gtk.Overlay widget for the main content area
        self.__layers[2][0].addLayoutContainer(self.__apps_dict[menuItemLabel.lower()].getLayoutContainer())

    def get_overlay(self):
        """ Accessor function: returns Gtk.Overlay object used for layering window content. """
        return self.__interface_layer

    def __build_default_interface(self):
        """ Initilization: composes layout of main gui.
            Expected arguments: [layer instance, layer order, input passthrough]
        """
        self.__layers.append([self.__notification_layer, 0, False])
        self.__layers.append([MenuLayer(self), 1, True])
        self.__layers.append([ContentLayer(self.__window_width, self.__window_height, self.__contentAreaDimensions), 2, True])
        self.__layers.append([self.__alert_layer, 3, False])
        self.__add_overlays()

        self.load_content_area(default_menu)      # default_menu is defined in Settings.py

    def __add_overlays(self):
        """ Private: Iterates over a list of widgets and adds them to a Gtk.Overlay widget """
        for layer in self.__layers:
            self.__add_display_layer(layoutContainer=layer[0].get_layout_container(), pass_through=layer[2])
        self.hide_alert_layer()     # Hide the alert layer by sending it to the bottom of the Overlay stack

    def show_alert_layer(self):
        """ Public: Moves the alert layer from the bottom of Gtk.Overlay stack to the top of the stack. """
        self.__interface_layer.reorder_overlay(self.__alert_layer.get_layout_container(), -1)

    def hide_alert_layer(self):
        """ Public: Moves the alert layer to the bottom of Gtk.Overlay stack in order to hide it. """
        self.__interface_layer.reorder_overlay(self.__alert_layer.get_layout_container(), 0)

    def __add_display_layer(self, layoutContainer, pass_through=False):
        """ Private: Adds a layout container to the Gtk.Overlay widget and sets the pass_through flag. """
        # Gtk uses set_overlay_pass_through() for passing input events through to underlying overlay layers ->
        self.__interface_layer.add_overlay(layoutContainer)
        if pass_through is True:
            self.__interface_layer.set_overlay_pass_through(layoutContainer, True)

    def process_message(self, message):
        """ Public: Passes incoming messages through to the router for processing. """
        self.__router.process_message(message=message)

    def send_message(self, message):
        """ Public: Passes outgoing messages through to the router for transmission. """
        self.__router.send_message(message=message)
