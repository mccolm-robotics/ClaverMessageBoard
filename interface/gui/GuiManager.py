import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from interface.gui.NotificationLayer import NotificationLayer
from interface.gui.MenuLayer import MenuLayer
from interface.gui.ContentLayer import ContentLayer
import interface.settings.Settings as settings
from interface.doodle.DoodleManager import DoodleManager
from interface.games.GamesManager import GamesManager
from interface.messages.MessagesManager import MessagesManager
from interface.photos.PhotosManager import PhotosManager
from interface.news.NewsManager import NewsManager
from interface.timer.TimerManager import TimerManager
from interface.calendar.CalendarManager import CalendarManager
from interface.lists.ListsManager import ListsManager
from interface.settings.SettingsManager import SettingsManager


class GuiManager:

    def __init__(self, window_width, window_height):
        """ Constructor """
        self.__window_width = window_width
        self.__window_height = window_height
        self.__interface_layer = Gtk.Overlay()
        self.__layers = []
        self.__updateCallbacks = []
        self.__contentAreaDimensions = [1, 1]
        self.__apps_dict = {
            settings.menu_labels[0][0]: DoodleManager(),
            settings.menu_labels[1][0]: GamesManager(),
            settings.menu_labels[2][0]: MessagesManager(),
            settings.menu_labels[3][0]: PhotosManager(),
            settings.menu_labels[4][0]: NewsManager(),
            settings.menu_labels[5][0]: TimerManager(),
            settings.menu_labels[6][0]: CalendarManager(),
            settings.menu_labels[7][0]: ListsManager(),
            settings.menu_labels[8][0]: SettingsManager(self)
        }
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
            self.__layers[2][0].removeLayoutContainer(self.__apps_dict[self.__activeMenu].getLayoutContainer())
            self.__activeMenu = menuItemLabel
            self.setBackgroundColour(settings.settings_menu_background_classes_dict[menuItemLabel])

        self.__layers[2][0].addLayoutContainer(self.__apps_dict[menuItemLabel].getLayoutContainer())

    def getOverlay(self):
        """ Accessor function: returns Gtk layout container """
        return self.__interface_layer

    def __build_default_interface(self):
        """ Initilization: composes layout of main gui """
        self.__layers.append([NotificationLayer(), 0, False])
        self.__layers.append([MenuLayer(self), 1, False])
        self.__layers.append([ContentLayer(self.__window_width, self.__window_height, self.__contentAreaDimensions), 2, True])
        self.__addOverlays()

        self.loadContentArea(settings.default_menu)

    def __addOverlays(self):
        for layer in self.__layers:
            self.__addDisplayLayer(layer[0].getLayoutContainer(), layer[2])

    def __addDisplayLayer(self, layoutContainer, pass_through=False):
        self.__interface_layer.add_overlay(layoutContainer)
        if pass_through is True:
            self.__interface_layer.set_overlay_pass_through(layoutContainer, True)

