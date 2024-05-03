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

import custwidg

if __name__ == "__main__":

    w = Gtk.Window()
    w.set_size_request(400, 300)
    w.connect("destroy", Gtk.main_quit)

    vbox = Gtk.VBox()
    hbox = Gtk.HBox()

    sw = custwidg.SimpleWidget()

    hbox.pack_start(Gtk.Label(label="  b "), 0, 0, 0)
    hbox.pack_start(sw, 1, 1, 0)
    hbox.pack_start(Gtk.Label(label="  e "), 0, 0, 0)

    vbox.pack_start(Gtk.Label(label="  t "), 0, 0, 0)
    vbox.pack_start(hbox, 1, 1, 0)
    vbox.pack_start(Gtk.Label(label="  b "), 0, 0, 0)

    butt = Gtk.Button.new_with_mnemonic("E_xit")
    butt.connect("clicked", Gtk.main_quit)
    vbox.pack_start(butt, 0, 0, 2)

    w.add(vbox)
    w.show_all()
    #w.present()

    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


