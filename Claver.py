"""
Author: McColm Robotics
Title: Simple window using GLADE
Created: April 2020
Python interpreter: 3.7
GTK3 version: 3.24
PyCharm version: 2020.1
"""
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys


class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        builder = Gtk.Builder()
        builder.add_from_file("RootWindow.glade")
        window = builder.get_object("RootWindow")
        window.set_application(self)
        builder.connect_signals(self)
        window.show_all()

    def on_button_clicked(self, widget):
        print("You clicked the damn button!")

# create and run the application, exit with the value returned by
# running the program
app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)