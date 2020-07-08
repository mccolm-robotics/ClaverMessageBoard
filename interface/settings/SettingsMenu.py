import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf
import interface.settings.Settings as settings

class SettingsMenu:
    def __init__(self, settingsManager):
        """ Constructor """
        self.__settingsManager = settingsManager
        self.__active_button = None
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__layoutContainer.get_style_context().add_class('settings-menu-panel')

        self.__build_content()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layoutContainer

    def getMenuBoxAllocation(self):
        return self.__layoutContainer.get_allocation()

    def __build_content(self):
        menu_label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        menu_label_box.set_margin_top(15)
        menu_label_box.set_margin_bottom(15)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=settings.res_dir['BUTTON_IMAGES'] + "Search.png",
            width=20,
            height=20,
            preserve_aspect_ratio=True)

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        search_button = Gtk.Button()
        search_button.add(image)
        search_button.set_can_focus(False)
        search_button.get_style_context().add_class('settings-menu-button-search')
        menu_label_box.add(search_button)

        menu_title = Gtk.Label()  # Add a label to the box
        menu_title.set_text("Settings")  # Set the value of the label text
        menu_title.get_style_context().add_class('settings-menu-title')  # Connect a CSS class to the label
        menu_label_box.add(menu_title)

        self.__layoutContainer.add(menu_label_box)
        self.__build_Button_list()

    def __build_Button_list(self):
        group = Gtk.RadioButton.new(None)
        for index, label in enumerate(settings.settings_menu_labels):
            button = Gtk.RadioButton.new_with_label_from_widget(group, label)
            button.get_style_context().add_class('settings-menu-button')
            button.set_mode(False)
            if index == 0:
                button.set_active(True)
                self.__active_button = label
            button.connect("toggled", self.on_button_toggled, label)
            self.__layoutContainer.add(button)

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.__setActiveMenu(name)

    def __setActiveMenu(self, name):
        self.__settingsManager.loadMenu(name)