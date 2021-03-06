import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from .Settings import *
from ..gui.CategoryManagerTemplate import CategoryManagerTemplate
from .SettingsMenu import SettingsMenu
from .categories.AboutMenu import AboutMenu
from .categories.AccountMenu import AccountMenu
from .categories.GeneralMenu import GeneralMenu
from .categories.NetworkMenu import NetworkMenu
from .categories.ThemeMenu import ThemeMenu


class SettingsManager(CategoryManagerTemplate):
    def __init__(self, guiManager, notification_manager):
        """ Constructor """
        super().__init__(guiManager)
        self.__contentAreaDimensions = [1, 1]
        self.__menuAreaDimensions = [1, 1]
        self.__menuContentSize = [1, 1]
        self.__active_menu = None
        self.__menu_dict = {
            settings_menu_labels[0]: GeneralMenu(),
            settings_menu_labels[1]: ThemeMenu(),
            settings_menu_labels[2]: NetworkMenu(),
            settings_menu_labels[3]: AccountMenu(),
            settings_menu_labels[4]: AboutMenu(self)
        }
        self.__layoutContainer = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_content()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layoutContainer

    def registerUpdateCallback(self, function):
        """ Callback registration: used by menu pages to receive updates about window resize events """
        super().registerUpdateCallback(function)

    @CategoryManagerTemplate.callback_on_resize
    def updateContentDimensions(self):
        """ Callback function: registered to receive updates from GuiManager when window resized """
        self.__contentAreaDimensions = super().getContentAreaSize()
        menu_rect = self.menu.getMenuBoxAllocation()
        self.__menuAreaDimensions = [menu_rect.width, menu_rect.height]
        self.__menuContentSize = [self.__contentAreaDimensions[0] - self.__menuAreaDimensions[0], self.__menuAreaDimensions[1]]
        super().updateCallbackFunctions(self.__menuContentSize)

    def __build_content(self):
        """ Initilization: composes layout of settings area """
        self.menu = SettingsMenu(self)
        menu_container = self.menu.getLayoutContainer()
        self.__layoutContainer.attach(child=menu_container, left=0, top=0, width=1, height=1)
        self.__content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)                        # Add a box below the message bar
        self.__content_area.set_hexpand(True)                                                      # Set box height to 100% of remaining space
        self.__content_area.set_vexpand(True)
        self.__layoutContainer.attach(child=self.__content_area, left=1, top=0, width=1, height=1)

        self.loadMenu(self.__active_menu)

    def loadMenu(self, menuLabel: str):
        """ Load and Initialize: switches out menu pages """
        if type(menuLabel) == str:
            menuLabel = menuLabel.capitalize()  # Ensure that the label is capitalized to match the label stored in settings_menu_labels[]
        if self.__active_menu == None:
            self.__active_menu = settings_menu_labels[0]
        else:
            self.__content_area.remove(self.__menu_dict[self.__active_menu].getLayoutContainer())
            self.__active_menu = menuLabel
        self.__content_area.add(self.__menu_dict[self.__active_menu].getLayoutContainer())
        self.__content_area.show_all()

