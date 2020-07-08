import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class NewsManager:
    def __init__(self):
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__build_content()

    def getLayoutContainer(self):
        return self.__layoutContainer

    def __build_content(self):
        label = Gtk.Label()  # Add a label to the box
        label.set_text("News Area")  # Set the value of the label text
        label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        self.__layoutContainer.add(label)
        button = Gtk.Button()
        button.set_label("Click Me News")
        self.__layoutContainer.add(button)