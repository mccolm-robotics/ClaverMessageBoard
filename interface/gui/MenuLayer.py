import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from interface.settings.Settings import *

class MenuLayer:

    NUM_NAV_BUTTONS = 9
    MENU_ALLOCATION = None

    def __init__(self, guiManager):
        """ Constructor """
        self.__guiManager = guiManager
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of menu area """
        self.__menu_buttons = []
        for i in range(self.NUM_NAV_BUTTONS):
            self.__menu_buttons.append(self.add_nav_button(i))

        self.__content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__content_area.set_hexpand(True)
        self.__content_area.set_vexpand(True)

        self.__layout_container.attach(child=self.__content_area, left=0, top=1, width=1, height=1)
        for index, button in enumerate(self.__menu_buttons, start=0):
            self.__layout_container.attach(child=button, left=1, top=index, width=1, height=1)

    def getContentBoxAllocation(self):
        return self.__content_area.get_allocation()

    def add_nav_button(self, buttonNum):
        """ Creates a GtkEventBox and Label for each menu button """

        if menu_labels[buttonNum][0] == default_menu:
            self.__activeButton = menu_labels[buttonNum][0]

        label = Gtk.Label()
        label.set_text(menu_labels[buttonNum][0])
        label.set_halign(Gtk.Align.START)
        label.get_style_context().add_class('nav-button-label')

        button = Gtk.EventBox()
        button.add(label)
        button.connect('button-press-event', self.on_nav_button_pressed)
        button.connect('button-release-event', self.on_nav_button_released)
        button.set_can_focus(False)
        button.connect("draw", self.draw_nav_button)
        button.set_vexpand(True)
        button.set_name(menu_labels[buttonNum][0])
        return button

    @staticmethod
    def draw_rounded_menu_button(context: object, x: object, y: object, width: object, height: object, radius: object, lineWidth: object, active: object) -> object:
        """ draws rectangles with rounded (circular arc) corners """

        from math import pi
        degrees = pi / 180

        context.set_line_width(lineWidth)
        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)  # Black

        context.move_to(width + lineWidth, height + lineWidth / 2)
        context.line_to(x + radius, height + lineWidth / 2)
        context.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)  # Bottom Left
        context.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)  # Top Left
        context.line_to(width + lineWidth, y)

        # context.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
        # context.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)

        # context.close_path()
        context.stroke_preserve()
        if active is False:
            context.set_source_rgba(81 / 255, 81 / 255, 81 / 255, 1.0)  # Gray
        else:
            context.set_source_rgba(32 / 255, 87 / 255, 122 / 255, 1.0)  # Teal
        context.fill()
        context.stroke()

    def draw_nav_button(self, widget, context):
        """ draws rectangles with rounded (circular arc) corners """

        if widget.get_children()[0].get_text() == self.__activeButton:
            active = True
        else:
            active = False

        alloc = widget.get_allocation()
        width = alloc.width
        height = alloc.height
        buttonRadius = 20
        xOffset = 0
        yOffset = 0

        # Create a surface to use as the input area for GtkEventBox
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        # Reset buffer background
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)  # Transparent black
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        outline_top_left_offset = theme_prefs['OUTLINE'] / 2
        outline_bottom_right_offset = theme_prefs['OUTLINE']

        # Draw to the Cairo buffer
        self.draw_rounded_menu_button(context=ctx, x=outline_top_left_offset + xOffset, y=outline_top_left_offset + yOffset,
                                      width=width - outline_bottom_right_offset,
                                      height=height - outline_bottom_right_offset, radius=buttonRadius,
                                      lineWidth=theme_prefs['OUTLINE'], active=active)
        # Draw to the widget surface
        self.draw_rounded_menu_button(context=context, x=outline_top_left_offset + xOffset,
                                      y=outline_top_left_offset + yOffset, width=width - outline_bottom_right_offset,
                                      height=height - outline_bottom_right_offset, radius=buttonRadius,
                                      lineWidth=theme_prefs['OUTLINE'], active=active)

        # save file
        # surface.write_to_png("MyImage.png")
        input_region = Gdk.cairo_region_create_from_surface(surface)
        widget.input_shape_combine_region(input_region)

    def on_nav_button_pressed(self, widget, event):
        if 'GDK_BUTTON_PRESS' in str(event.type):  # If the user made a "single click"
            if event.button == Gdk.BUTTON_PRIMARY:  # If it is a left click
                # https://developer.gnome.org/gtk3/stable/GtkContainer.html
                self.__activeButton = widget.get_children()[0].get_text()
                self.__guiManager.loadContentArea(widget.get_children()[0].get_text())
                # print(widget.get_name())  # Lots of latency on this function
                widget.get_toplevel().queue_draw()

    def on_nav_button_released(self, widget, event):
        pass