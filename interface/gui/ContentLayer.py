import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class ContentLayer:

    def __init__(self, window_width, window_height, dimensions):
        """ Constructor """
        self.__window_width = window_width
        self.__window_height = window_height
        self.__contentAreaDimensions = dimensions

        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of content area """
        self.__content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)                        # Add a box below the message bar
        self.__content_area.set_hexpand(True)                                                      # Set box height to 100% of remaining space
        self.__content_area.set_vexpand(True)
        self.__content_area.set_margin_right(self.__window_width - self.__contentAreaDimensions[0])
        self.__content_area.set_margin_top(self.__window_height - self.__contentAreaDimensions[1])
        self.__layout_container.attach(child=self.__content_area, left=0, top=0, width=1, height=1)   # Attach this box to the layout below the message bar

    def addLayoutContainer(self, container):
        self.__content_area.add(container)
        container.show_all()

    def removeLayoutContainer(self, container):
        self.__content_area.remove(container)

    def updateContentAreaDimensions(self, window_width, window_height):
        self.__window_width = window_width
        self.__window_height = window_height

        self.__content_area.set_margin_right(self.__window_width - self.__contentAreaDimensions[0])
        self.__content_area.set_margin_top(self.__window_height - self.__contentAreaDimensions[1])
