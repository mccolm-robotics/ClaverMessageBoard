import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class ThemeMenu:
    def __init__(self):
        self.__layoutContainer = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_content()

    def getLayoutContainer(self):
        return self.__layoutContainer

    def __build_content(self):
        category_title = Gtk.Label()  # Add a label to the box
        category_title.set_hexpand(True)    # Set the label width to 100%
        category_title.set_text("Theme Settings")  # Set the value of the label text
        category_title.get_style_context().add_class('cat-menu-title')  # Connect a CSS class to the label

        self.__layoutContainer.attach(child=category_title, left=0, top=0, width=1, height=1)   # Add label to top of grid container