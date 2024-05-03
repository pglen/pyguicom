#!/usr/bin/env python3

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

import pgsimp
import pggui
import pgutils

def subdialog(arg2):

    def pressed(arg2, arg3):
        #print("pressed")
        pggui.message("From sub", parent=arg3)
    def pressed2(arg2, arg3):
        #print("pressed2", arg2, arg3)
        arg3.response(Gtk.ResponseType.OK)
        arg3.destroy()

    dialog = Gtk.Dialog()
    dialog.set_size_request(200, 100)
    dialog.add_button = (Gtk.ButtonsType.CLOSE, Gtk.ResponseType.OK)
    bbb = Gtk.Button("Message")
    dialog.vbox.pack_start(bbb, 0, 0, 0)
    bbb.connect("pressed", pressed, dialog)
    #buttons=Gtk.ButtonsType.CLOSE)
    bbb = Gtk.Button.new_with_mnemonic("E_xit Sub")
    dialog.vbox.pack_start(bbb, 0, 0, 0)
    bbb.connect("pressed", pressed2, dialog)
    dialog.show_all()
    dialog.run()

# ------------------------------------------------------------------------
class testwin(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        #self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("unmap", Gtk.main_quit)

# ------------------------------------------------------------------------

class pgtestwin(testwin):

    def __init__(self):

        testwin.__init__(self)

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

        #butt = Gtk.Button.new_with_mnemonic("Test Yes_no _cancel2")
        #butt.connect("clicked", self.test_yes_no_cancel2)
        #vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test Yes_no _cancel")
        butt.connect("clicked", self.test_yes_no_cancel)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test Yes_no")
        butt.connect("clicked", self.test_yes_no)
        vbox.pack_start(butt, 0, 0, 2)

        #butt = Gtk.Button.new_with_mnemonic("Test Yes_no2")
        #butt.connect("clicked", self.test_yes_no2)
        #vbox.pack_start(butt, 0, 0, 2)
        #
        #butt = Gtk.Button.new_with_mnemonic("Test M_essage2")
        #butt.connect("clicked", self.test_message2)
        #vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test M_essage")
        butt.connect("clicked", self.test_message)
        vbox.pack_start(butt, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("Test Sub Dialog")
        butt.connect("clicked", subdialog)
        vbox.pack_start(butt, 0, 0, 2)


        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

    def test_about(self, arg2):
        print(pgutils.about("Tester"))

    def test_yes_no_cancel2(self, arg2):
        print(pggui.yes_no_cancel2("Yes No Message"))

    def test_yes_no_cancel(self, arg2):
        print(pggui.yes_no_cancel("Yes No Message"))

    def test_yes_no(self, arg2):
        print(pggui.yes_no("Yes No Message"))

    def test_yes_no2(self, arg2):
        print(pggui.yes_no2("Yes No Message"))

    def test_message2(self, arg2):
        pggui.message2("Hello Message")

    def test_message(self, arg2):
        pggui.message("Hello Message")


tw = pgtestwin()

#print("test")

Gtk.main()

# EOF
