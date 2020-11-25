import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .AlertLayer import AlertLayer
from .ContentLayer import ContentLayer
from .MenuLayer import MenuLayer
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

    def __init__(self, window_width, window_height, message_queue):
        """ Constructor """
        self.__window_width = window_width
        self.__window_height = window_height
        self.__alert_layer = AlertLayer()
        self.__notification_layer = NotificationLayer()
        self.__notification_manager = NotificationManager(self.__notification_layer, self.__alert_layer)
        self.queue = message_queue
        self.__interface_layer = Gtk.Overlay()
        self.__layers = []
        self.__updateCallbacks = []
        self.__contentAreaDimensions = [1, 1]
        self.__apps_dict = {
            # This is probably a bad idea if the labels are changed into a different character set
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
        self.__router = Router(message_queue=self.queue, notification_manager=self.__notification_manager, mode_objects=self.__apps_dict)
        self.__activeMenu = None
        self.__build_default_interface()

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
        self.__layers[0][0].setBackgroundColour(css_class)

    def loadContentArea(self, menuItemLabel):
        if self.__activeMenu is None:
            self.__activeMenu = menuItemLabel
        else:
            self.__layers[2][0].removeLayoutContainer(self.__apps_dict[self.__activeMenu.lower()].getLayoutContainer())
            self.__activeMenu = menuItemLabel
            self.setBackgroundColour(settings_menu_background_classes_dict[menuItemLabel])

        self.__layers[2][0].addLayoutContainer(self.__apps_dict[menuItemLabel.lower()].getLayoutContainer())

    def getOverlay(self):
        """ Accessor function: returns Gtk layout container """
        return self.__interface_layer

    def __build_default_interface(self):
        """ Initilization: composes layout of main gui.

        expected arguments [layer instance, layer order, input passthrough]
        """
        self.__layers.append([self.__notification_layer, 0, False])
        self.__layers.append([MenuLayer(self), 1, False])
        self.__layers.append([ContentLayer(self.__window_width, self.__window_height, self.__contentAreaDimensions), 2, True])
        self.__layers.append([self.__alert_layer, 3, False])
        self.__addOverlays()

        self.loadContentArea(default_menu)

    def __addOverlays(self):
        for layer in self.__layers:
            self.__addDisplayLayer(layoutContainer=layer[0].getLayoutContainer(), pass_through=layer[2])

    def __addDisplayLayer(self, layoutContainer, pass_through=False):
        # Gtk has a special function for passing input events through to underlying overlay layers
        self.__interface_layer.add_overlay(layoutContainer)
        if pass_through is True:
            self.__interface_layer.set_overlay_pass_through(layoutContainer, True)

    def process_message(self, message):
        self.__router.process_message(message=message)

    def send_message(self, message):
        self.__router.send_message(message=message)
