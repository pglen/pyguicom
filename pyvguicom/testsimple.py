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
import pgutils
import pgtests

# ------------------------------------------------------------------------
class testwin(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        #self.set_default_size(1024, 768)
        self.set_default_size(800, 600)
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
        hbox5.pack_start(self.label, 1, 1, 2)

        vbox  = Gtk.VBox()

        self.treeview = pgsimp.SimpleTree(("Hour", "Subject", "Alarm", "Notes"))
        frame2 = pgutils.wrapscroll(self.treeview)
        hbox.pack_start(frame2, 1, 1, 2)

        self.editor = pgsimp.SimpleEdit()
        frame3 = pgutils.wrapscroll(self.editor)
        hbox.pack_start(frame3, 1, 1, 2)

        vbox.pack_start(hbox3, 0, 0, 2)
        vbox.pack_start(hbox2, 0, 0, 2)
        vbox.pack_start(hbox4, 0, 0, 2)
        vbox.pack_start(hbox, 1, 1, 2)
        vbox.pack_start(hbox5, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

tw = pgtestwin()

#print("test")

def fillrand():
    aaa = []
    for aa in range(10):
        aaa.append( (pgtests.randstr(12), pgtests.randstr(12),
                        pgtests.randstr(12), pgtests.randstr(12)) )
    return aaa

aaa = fillrand()
tw.treeview.clear()
for aa in aaa:
    try:
        tw.treeview.append(aa)
    except:
        print(sys.exc_info())

tw.editor.clear()

for aa in aaa:
    try:
        tw.editor.append(str(aa) + "\n")
    except:
        print(sys.exc_info())


Gtk.main()

# EOF
