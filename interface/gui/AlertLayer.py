import re

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk
from ..settings.Settings import *

class CodeEntryBox(Gtk.Entry, Gtk.Editable):
    """ Custom GTK Entry box:

    Python bindings for GTK throw a warning when connecting to the insert_text signal on an
    Entry box. This stems from bug 644927 in the pygobject implementation and arises due to its handling of in/out
    parameters. This function overrides the base implementation provided by Gtk.Editable, which is called by Gtk.Entry,
    in order to only override the local copy of the base implementation and not every other instance of Gtk.Entry in the
    application."""

    def __init__(self, alert_layer=None, id=None):
        """ Constructor """
        super(CodeEntryBox, self).__init__()
        self.id = id
        self.alert_layer = alert_layer

    def do_insert_text(self, new_text, length, position):
        """ Overrides the default handler for insert_text signals. """
        self.get_buffer().insert_text(position, new_text, length)
        next_box = self.alert_layer.get_entry_box(self.id + 1)
        if next_box is not None:
            next_box.grab_focus()
        else:
            print("Done")
        return position + length

class AlertLayer:
    def __init__(self):
        """ Constructor """
        self.__default_css_class = default_css_class
        self.__layout_container = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__build_layer()

    def getLayoutContainer(self):
        """ Accessor function: returns Gtk layout container """
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of menu area """
        alert_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        alert_area.set_hexpand(True)
        alert_area.set_vexpand(True)
        alert_area.get_style_context().add_class('alert-background')

        alert_box = Gtk.Box()  # Create a new label
        # alert_box.set_text("This is an alert")  # Set the value of the label text
        alert_box.get_style_context().add_class('alert')  # Connect a CSS class to the label
        # alert_box.set_hexpand(True)
        alert_box.set_vexpand(True)
        alert_box.set_halign(Gtk.Align.CENTER)
        alert_box.set_valign(Gtk.Align.CENTER)
        alert_area.add(alert_box)

        alert_box_content = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        alert_box.add(alert_box_content)

        notification_label = Gtk.Label()  # Create a new label
        notification_label.set_text("Authorization code")  # Set the value of the label text
        notification_label.set_hexpand(True)
        notification_label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        alert_box_content.attach(child=notification_label, left=0, top=0, width=1, height=1)

        entry_grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        alert_box_content.attach(child=entry_grid, left=0, top=1, width=1, height=1)

        self.entry_boxes = []
        for i in range(7):
            self.entry_boxes.append(CodeEntryBox(alert_layer=self, id=i))
            self.entry_boxes[i].set_max_length(1)
            self.entry_boxes[i].set_max_width_chars(1)
            self.entry_boxes[i].set_width_chars(1)
            self.entry_boxes[i].set_alignment(0.5)
            self.entry_boxes[i].get_style_context().add_class('authorization-code-box')
            entry_grid.attach(child=self.entry_boxes[i], left=i, top=0, width=1, height=1)

        self.__layout_container.attach(child=alert_area, left=0, top=0, width=1, height=1)

    def get_entry_box(self, index):
        if index < len(self.entry_boxes):
            return self.entry_boxes[index]

    def getContentBoxAllocation(self):
        return self.__content_area.get_allocation()

"""
Resources: GTK Entry boxes
# https://stackoverflow.com/questions/40074977/how-to-format-the-entries-in-gtk-entry
# https://stackoverflow.com/questions/38815694/gtk-3-position-attribute-on-insert-text-signal-from-gtk-entry-is-always-0
"""