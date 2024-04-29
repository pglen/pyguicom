#!/usr/bin/env python

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
import pgutils

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

        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

    def test_about(self, arg2):
        print(pgutils.about("Tester"))

    def test_yes_no_cancel2(self, arg2):
        print(pgutils.yes_no_cancel2("Yes No Message"))

    def test_yes_no_cancel(self, arg2):
        print(pgutils.yes_no_cancel("Yes No Message"))

    def test_yes_no(self, arg2):
        print(pgutils.yes_no("Yes No Message"))

    def test_yes_no2(self, arg2):
        print(pgutils.yes_no2("Yes No Message"))

    def test_message2(self, arg2):
        pgutils.message2("Hello Message")

    def test_message(self, arg2):
        pgutils.message("Hello Message")


tw = pgtestwin()

#print("test")

def fillrand():
    aaa = []
    for aa in range(10):
        aaa.append( (pgutils.randstr(12), pgutils.randstr(12),
                        pgutils.randstr(12), pgutils.randstr(12)) )
    return aaa

Gtk.main()

# EOF
