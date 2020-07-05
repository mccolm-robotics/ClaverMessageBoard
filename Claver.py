import sys

import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from interface.Settings import *

class Claver_Main(Gtk.Application):

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    NUM_NAV_BUTTONS = 9

    def __init__(self):
        Gtk.Application.__init__(self)

        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(res_dir['CSS_MAIN'] + 'style.css')
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.__activeButton = None


    def do_activate(self):
        """ Initializes the application window """

        self.window = Gtk.Window(application=self)
        self.window.set_title("Claver Communication Board")
        self.window.set_default_size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("size-allocate", self.on_resize)

        # Create a layer object
        interface_layer = Gtk.Overlay()
        self.window.add(interface_layer)

        # Messages-bar layer (bottom)
        message_layer_layout = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)  # Create a grid to manage containers
        interface_layer.add_overlay(message_layer_layout)                                           # Add to the layer object
        message_layer_top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)                     # Add a box to contain messages
        message_layer_top_bar.get_style_context().add_class('message-bar')                          # Connect CSS class to box
        message_layer_top_bar.set_hexpand(True)                                                     # Set the box to expand 100%
        label = Gtk.Label()                                                                         # Add a label to the box
        label.set_text("Notifications")                                                             # Set the value of the label text
        label.get_style_context().add_class('label-notification')                                   # Connect a CSS class to the label
        message_layer_top_bar.add(label)                                                            # Add the label into the box
        message_layer_layout.attach(child=message_layer_top_bar, left=0, top=0, width=1, height=1)  # Attach the box to the layout at o, 0
        message_layer_bottom = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)                        # Add a box below the message bar
        message_layer_bottom.set_hexpand(True)                                                      # Set box height to 100% of remaining space
        message_layer_bottom.set_vexpand(True)
        message_layer_bottom.get_style_context().add_class('main-grid')                             # Connect a CSS class to the box (background colour)
        message_layer_layout.attach(child=message_layer_bottom, left=0, top=1, width=1, height=1)   # Attach this box to the layout below the message bar

        # Navigation-menu layer
        grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        interface_layer.add_overlay(grid)

        self.__menu_buttons = []
        for i in range(self.NUM_NAV_BUTTONS):
            self.__menu_buttons.append(self.add_nav_button(i))

        vbox_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox_list.set_hexpand(True)
        vbox_list.set_vexpand(True)
        vbox_list.set_valign(Gtk.Align.END)

        grid.attach(child=vbox_list, left=0, top=1, width=1, height=1)
        for index, button in enumerate(self.__menu_buttons, start=0):
            grid.attach(child=button, left=1, top=index, width=1, height=1)

        self.window.show_all()

    def on_resize(self, window, size_rect):
        width = size_rect.width
        height = size_rect.height
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height

    def add_nav_button(self, buttonNum):
        """ Creates a GtkEventBox and Label for each menu button """

        if button_labels[buttonNum][1] is True:
            self.__activeButton = button_labels[buttonNum][0]

        label = Gtk.Label()
        label.set_text(button_labels[buttonNum][0])
        label.set_halign(Gtk.Align.START)
        label.get_style_context().add_class('nav-button-label')

        button = Gtk.EventBox()
        button.add(label)
        button.connect('button-press-event', self.on_nav_button_pressed)
        button.connect('button-release-event', self.on_nav_button_released)
        button.connect("draw", self.draw_nav_button)
        button.set_vexpand(True)
        button.set_name(button_labels[buttonNum][0])

        return button

    def draw_rounded_menu_button(self, context, x, y, width, height, radius, lineWidth, active):
        """ draws rectangles with rounded (circular arc) corners """

        from math import pi
        degrees = pi / 180

        context.set_line_width(lineWidth)
        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)     # Black

        context.move_to(width + lineWidth, height + lineWidth/2)
        context.line_to(x + radius, height + lineWidth/2)
        context.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)   # Bottom Left
        context.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)             # Top Left
        context.line_to(width + lineWidth, y)

        # context.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
        # context.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)

        # context.close_path()
        context.stroke_preserve()
        if active is False:
            context.set_source_rgba(81/255, 81/255, 81/255, 1.0)    # Gray
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
        self.draw_rounded_menu_button(context=ctx, x=outline_top_left_offset + xOffset, y=outline_top_left_offset + yOffset, width=width - outline_bottom_right_offset, height=height - outline_bottom_right_offset, radius=buttonRadius, lineWidth=theme_prefs['OUTLINE'], active=active)
        # Draw to the widget surface
        self.draw_rounded_menu_button(context=context, x=outline_top_left_offset + xOffset, y=outline_top_left_offset + yOffset, width=width - outline_bottom_right_offset, height=height - outline_bottom_right_offset, radius=buttonRadius, lineWidth=theme_prefs['OUTLINE'], active=active)

        # save file
        # surface.write_to_png("MyImage.png")
        input_region = Gdk.cairo_region_create_from_surface(surface)
        widget.input_shape_combine_region(input_region)

    def on_nav_button_pressed(self, widget, event):
        if 'GDK_BUTTON_PRESS' in str(event.type):   # If the user made a "single click"
            if event.button == Gdk.BUTTON_PRIMARY:  # If it is a left click
                # https://developer.gnome.org/gtk3/stable/GtkContainer.html
                self.__activeButton = widget.get_children()[0].get_text()
                print(widget.get_children()[0].get_text())
                # print(widget.get_name())  # Lots of latency on this function
                self.window.queue_draw()

    def on_nav_button_released(self, widget, event):
        pass

if __name__ == "__main__":
    application = Claver_Main()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)