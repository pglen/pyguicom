#!/usr/bin/env python3

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango

gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

import pgtests

def test_randstr(arg2, arg3):
    rrr = pgtests.randstr(12)
    print(rrr)
    arg3.set_text(rrr)

def test_randstrrand(arg2, arg3):
    rrr = pgtests.randstrrand(6, 18)
    print(rrr)
    arg3.set_text(rrr)

def test_rand(arg2, arg3):
    rrr = pgtests.randascii(12)
    print(rrr)
    arg3.set_text(rrr)

def test_rand2(arg2, arg3):
    rrr = pgtests.randisodate()
    print(rrr)
    arg3.set_text(rrr)

def test_rand3(arg2, arg3):
    rrr = pgtests.simname(12)
    print(rrr)
    arg3.set_text(rrr)

def test_rand4(arg2, arg3):
    rrr = pgtests.randate()
    print(rrr)
    arg3.set_text(rrr)

if __name__ == "__main__":

    w = Gtk.Window()
    w.set_size_request(400, 300)
    w.connect("destroy", Gtk.main_quit)

    vbox = Gtk.VBox()
    hbox = Gtk.HBox()

    lab1 = Gtk.Label(label="Test Label")
    hbox.pack_start(lab1, 1, 1, 0)
    vbox.pack_start(hbox, 1, 1, 0)

    butt = Gtk.Button.new_with_mnemonic("Test Rand Str")
    butt.connect("clicked", test_randstr, lab1)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test Rand Rand")
    butt.connect("clicked", test_randstrrand, lab1)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test Rand")
    butt.connect("clicked", test_rand, lab1)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test randisodate")
    butt.connect("clicked", test_rand2, lab1)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test simname")
    butt.connect("clicked", test_rand3, lab1)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test randdate")
    butt.connect("clicked", test_rand4, lab1)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("E_xit")
    butt.connect("clicked", Gtk.main_quit)
    vbox.pack_start(butt, 0, 0, 2)

    w.add(vbox)
    w.show_all()
    #w.present()

    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


