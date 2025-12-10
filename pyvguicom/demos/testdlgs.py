#!/usr/bin/env python3

import os, sys, warnings

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

sys.path.append(".")

from pyvguicom import pgutils

import pgsimp
import pggui
import pgdlgs

warnings.simplefilter("default")

def subdialog(arg2):

    def pressed(arg2, arg3):
        #print("pressed")
        pgdlgs.message("From sub", parent=arg3)

    def pressed2(arg2, arg3):
        #print("pressed2", arg2, arg3)
        arg3.response(Gtk.ResponseType.OK)
        arg3.destroy()

    dialog = Gtk.Dialog()
    dialog.set_size_request(250, -1)
    #dialog.add_button = (Gtk.ButtonsType.CLOSE, Gtk.ResponseType.OK)

    bbb = Gtk.Button(label="Message")
    bbb.connect("pressed", pressed, dialog)

    ccc = Gtk.Button.new_with_mnemonic("E_xit Sub")
    ccc.connect("pressed", pressed2, dialog)
    ccc.connect("clicked", pressed2, dialog)

    dialog.vbox.pack_start(bbb, 0, 0, 0)
    dialog.vbox.pack_start(ccc, 0, 0, 0)

    dialog.show_all()
    dialog.run()

class pgtestwin(Gtk.Window):

    def __init__(self):

        super(Gtk.Window, self).__init__()

        self.set_default_size(250, -1)

        hbox  = Gtk.HBox(); hbox3 = Gtk.HBox()
        hbox2 = Gtk.HBox(); hbox4 = Gtk.HBox()
        hbox5 = Gtk.HBox()

        self.label = Gtk.Label.new("Test strings here")
        hbox5.pack_start(self.label, 0, 0, 2)

        vbox  = Gtk.VBox()

        #vbox.pack_start(Gtk.Label(label="hello"), 1, 1, 2)

        butt = Gtk.Button.new_with_mnemonic("Test about")
        butt.connect("clicked", self.test_about)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test Yes No (yes)")
        butt.connect("clicked", self.test_yes_no)
        vbox.pack_start(butt, 0, 0, 2)

        butt3 = Gtk.Button.new_with_mnemonic("Test Yes No (no)")
        butt3.connect("clicked", self.test_yes_no2)
        vbox.pack_start(butt3, 0, 0, 2)

        butt2 = Gtk.Button.new_with_mnemonic("Test Yes no cancel (yes)")
        butt2.connect("clicked", self.test_yes_no_cancel)
        vbox.pack_start(butt2, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test Yes no cancel (no)")
        butt.connect("clicked", self.test_yes_no_cancel2)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test Yes no cancel (cancel)")
        butt.connect("clicked", self.test_yes_no_cancel3)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test M_essage")
        butt.connect("clicked", self.test_message)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test _Sub Dialog")
        butt.connect("clicked", subdialog)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

    def test_about(self, arg2):
        pgdlgs.about("Tester")

    def test_yes_no(self, arg2):
        pgdlgs.yes_no("Yes No Message")

    def test_yes_no2(self, arg2):
        pgdlgs.yes_no("Yes No Message", default="No")

    def test_yes_no_cancel(self, arg2):
        pgdlgs.yes_no_cancel("Yes No Message")

    def test_yes_no_cancel2(self, arg2):
        pgdlgs.yes_no_cancel("Yes No Message", default="No")

    def test_yes_no_cancel3(self, arg2):
        pgdlgs.yes_no_cancel("Yes No Message", default="Cancel")

    def test_message(self, arg2):
        pgdlgs.message("Hello Message")

pgtestwin()
Gtk.main()

# EOF
