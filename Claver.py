import sys

import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from interface.Settings import res_dir, theme_prefs

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


    def do_activate(self):
        """ Initializes a new window """

        window = Gtk.Window(application=self)
        window.set_title("Claver Communication Board")
        window.set_default_size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        window.set_position(Gtk.WindowPosition.CENTER)


        grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        window.add(grid)

        menu_buttons = []
        for i in range(self.NUM_NAV_BUTTONS):
            menu_buttons.append(self.add_nav_button(i, self.WINDOW_WIDTH / 5, self.WINDOW_HEIGHT / self.NUM_NAV_BUTTONS))

        vbox_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox_list.set_hexpand(True)
        vbox_list.set_vexpand(True)
        vbox_list.set_valign(Gtk.Align.END)

        grid.attach(vbox_list, 0, 1, 1, 1)
        for index, button in enumerate(menu_buttons, start=0):
            grid.attach(button, 1, index, 1, 1)

        grid.get_style_context().add_class('main-grid')

        window.show_all()

    def add_nav_button(self, buttonNum, width, height):

        label = Gtk.Label()
        label.set_text("Button {}".format(buttonNum))

        button = Gtk.EventBox()
        button.add(label)
        # RUN_Button.connect("clicked", self.button_clicked)
        # RUN_Button.get_style_context().add_class('button-background')
        button.set_name("myButton_green")
        button.connect('button-press-event', self.on_eventbox_pressed)
        button.connect('button-release-event', self.on_eventbox_released)
        button.connect("draw", self.draw_nav_button)
        button.set_size_request(width, height)
        return button

    def draw_rounded_menu_button(self, context, x, y, width, height, radius, lineWidth):
        """ draws rectangles with rounded (circular arc) corners """
        from math import pi
        degrees = pi / 180

        context.set_line_width(lineWidth)
        context.set_source_rgba(0.5, 0.0, 0.0, 1.0)     # Red

        context.move_to(width + lineWidth, height + lineWidth/2)
        context.line_to(x + radius, height + lineWidth/2)
        context.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)   # Bottom Left
        context.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)             # Top Left
        context.line_to(width + lineWidth, y)

        # context.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
        # context.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)

        # context.close_path()
        context.stroke_preserve()
        context.set_source_rgba(0.0, 0.5, 0.5, 1.0)
        context.fill()
        context.stroke()

    def draw_nav_button(self, widget, context, xOffset=0, yOffset=0):
        """ draws rectangles with rounded (circular arc) corners """
        alloc = widget.get_allocation()
        width = alloc.width
        height = alloc.height

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)

        # Reset buffer background
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)  # Transparent black
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        outline_top_left_offset = theme_prefs['OUTLINE'] / 2
        outline_bottom_right_offset = theme_prefs['OUTLINE']

        # Draw to the Cairo buffer
        self.draw_rounded_menu_button(context=ctx, x=outline_top_left_offset + xOffset, y=outline_top_left_offset + yOffset, width=width - outline_bottom_right_offset, height=height - outline_bottom_right_offset, radius=15, lineWidth=theme_prefs['OUTLINE'])
        # Draw to the widget surface
        self.draw_rounded_menu_button(context=context, x=outline_top_left_offset + xOffset, y=outline_top_left_offset + yOffset, width=width - outline_bottom_right_offset, height=height - outline_bottom_right_offset, radius=15, lineWidth=theme_prefs['OUTLINE'])

        # save file
        # surface.write_to_png("MyImage.png")
        input_region = Gdk.cairo_region_create_from_surface(surface)
        widget.input_shape_combine_region(input_region)

    def on_eventbox_pressed(self, widget, event):
        if 'GDK_BUTTON_PRESS' in str(event.type):   # If the user made a "single click"
            if event.button == 1:                   # if it is a left click
                print("button pressed")

    def on_eventbox_released(self, widget, event):
        print("button released")

if __name__ == "__main__":
    application = Claver_Main()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)