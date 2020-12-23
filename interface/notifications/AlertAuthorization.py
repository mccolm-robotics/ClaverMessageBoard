import subprocess
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from ..settings.Settings import *
from ..system.Transaction import Transaction

class AlertAuthorization(Transaction):
    """ Creates a gui interface for accepting a Claver authorization code. This object is initialized by the
    NotificationManager and implements the Transaction processing function used for processing messages received from
    the router."""
    def __init__(self, gui_manager):
        super().__init__(gui_manager.get_router())
        self.__gui_manager = gui_manager
        self.__build_layer()

    def get_content(self):
        return self.__layout_container

    def __build_layer(self):
        """ Initilization: composes layout of alert area """
        # A smaller box. Size set in CSS. Centered in background box
        self.__layout_container = Gtk.Box()  # Create a new layout box
        # self.__layout_container.set_text("This is an alert")  # Set the value of the label text
        self.__layout_container.get_style_context().add_class('alert')  # Connect a CSS class to the box
        # self.__layout_container.set_hexpand(True)
        self.__layout_container.set_vexpand(True)
        self.__layout_container.set_halign(Gtk.Align.CENTER)
        self.__layout_container.set_valign(Gtk.Align.CENTER)

        # Adds a layout grid to the smaller box to contain the alert title and data
        self.alert_box_content = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.__layout_container.add(self.alert_box_content)

        # Title of the Alert Window
        notification_label = Gtk.Label()  # Create a new label
        notification_label.set_text("Enter Authentication Code")  # Set the value of the label text
        notification_label.set_hexpand(True)
        notification_label.get_style_context().add_class('alert-title')  # Connect a CSS class to the label
        self.alert_box_content.attach(child=notification_label, left=0, top=0, width=1, height=1)

        # Grid containing the entry boxes for authorization code
        entry_grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.alert_box_content.attach(child=entry_grid, left=0, top=1, width=1, height=1)

        self.entry_boxes = []
        for i in range(7):
            self.entry_boxes.append(CodeEntryBox(alert_layer=self, id=i))
            self.entry_boxes[i].set_max_length(1)
            self.entry_boxes[i].set_max_width_chars(1)
            self.entry_boxes[i].set_width_chars(1)
            self.entry_boxes[i].set_alignment(0.5)
            self.entry_boxes[i].get_style_context().add_class('authorization-code-box')
            entry_grid.attach(child=self.entry_boxes[i], left=i, top=0, width=1, height=1)

        # A smaller box. Size set in CSS. Centered in background box
        results_box = Gtk.Box()  # Create a new layout box
        # results_box.set_text("This is an alert")  # Set the value of the label text
        # results_box.get_style_context().add_class('alert')  # Connect a CSS class to the box
        results_box.set_hexpand(True)
        results_box.set_vexpand(True)
        results_box.set_halign(Gtk.Align.START)
        results_box.set_valign(Gtk.Align.START)
        results_box.get_style_context().add_class('alert-results-box')
        self.alert_box_content.attach(child=results_box, left=0, top=2, width=1, height=1)

        # Text area for information on authentication process
        self.result_output = Gtk.Label()
        self.result_output.set_hexpand(True)
        self.result_output.set_vexpand(True)
        self.result_output.set_halign(Gtk.Align.START)
        self.result_output.set_valign(Gtk.Align.START)
        self.result_output.set_line_wrap(True)
        self.result_output.set_max_width_chars(60)
        ip_address_check = subprocess.run(["curl", "https://ipinfo.io/ip"], capture_output=True, encoding="utf-8")
        if ip_address_check.stdout:
            ip_address = ip_address_check.stdout
        else:
            ip_address = "ERROR"
        self.set_result_output(f"<big><b>Obtain Code From Web Portal</b></big>:\n1) Log in to the Claver web portal and click "
                               f"on 'Add Device'.\n2) Enter your device serial number and IP address.\n3)"
                               f" Input authentication code above.\n\nSerial #: {get_rpi_serial()} \n"
                               f"IP Address: {ip_address}")
        results_box.add(self.result_output)

        # Grid area for action buttons
        button_grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
        self.alert_box_content.attach(child=button_grid, left=0, top=3, width=1, height=1)

        # Action button - close alert
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", self.button_clicked)
        close_button.set_hexpand(True)
        close_button.get_style_context().add_class('alert-button')
        # close_button.set_name("myButton_green")
        button_grid.attach(child=close_button, left=0, top=3, width=1, height=1)

    def button_clicked(self, button):
        """ Callback for Gtk.Button event """
        if button.get_label() == "Close":
            self.__gui_manager.close_alert_layer()

    def confirm_code(self):
        """ Triggered when a value is entered into the final entry box """
        # Note: Does not check if all entry boxes contain values before verifying code. Length of code should be 7

        code = ""
        for i in range(7):
            code += self.entry_boxes[i].get_text()

        # self.result_output.get_style_context().add_class('result_output')
        # self.result_output.set_hexpand(True)
        # self.result_output.set_vexpand(True)
        # self.result_output.set_halign(Gtk.Align.START)
        # self.result_output.set_valign(Gtk.Align.START)
        self.set_result_output(f"<big><b>Confirming Code</b></big>:\n{code}")
        # self.result_output.show()

    def set_result_output(self, message):
        """ Sets text value for result output Gtk.Label """
        self.result_output.set_markup(message)

    def get_entry_box(self, index):
        """ Returns Gtk.Entry at index """
        if index < len(self.entry_boxes):
            return self.entry_boxes[index]

    def message_processor(self, message):
        print(f"Authorize Node: {message}")



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
            self.alert_layer.confirm_code()
        return position + length




"""
Resources: GTK Entry boxes
# https://stackoverflow.com/questions/40074977/how-to-format-the-entries-in-gtk-entry
# https://stackoverflow.com/questions/38815694/gtk-3-position-attribute-on-insert-text-signal-from-gtk-entry-is-always-0
"""