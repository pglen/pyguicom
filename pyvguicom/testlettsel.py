#!/usr/bin/env python

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

from pgsimp import *
from pgutils import *

# ------------------------------------------------------------------------
class testwin(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        #self.set_default_size(1024, 768)
        #self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("unmap", Gtk.main_quit)

def wrapscroll(what):

    scroll2 = Gtk.ScrolledWindow()
    scroll2.add(what)
    frame2 = Gtk.Frame()
    frame2.add(scroll2)
    return frame2

# ------------------------------------------------------------------------

class pgtestwin(testwin):

    def __init__(self):

        testwin.__init__(self)

        hbox  = Gtk.HBox();
        hbox2 = Gtk.HBox();
        hbox5 = Gtk.HBox()

        vbox  = Gtk.VBox()

        self.selector = LetterNumberSel(self.letterfilter, "Mono 16", " ")
        self.selector.set_tooltip_text("Arrow key to navigate, enter / space key to filter")

        hbox2.pack_start(Gtk.Label.new("  "), 0, 0, 2)
        hbox2.pack_start(self.selector , 1, 1, 2)
        hbox2.pack_start(Gtk.Label.new("  "), 0, 0, 2)

        vbox.pack_start(hbox2, 0, 0, 2)

        vbox.pack_start(hbox, 1, 1, 2)

        self.label = Gtk.Label.new("Test strings here")
        hbox5.pack_start(self.label, 1, 1, 2)
        vbox.pack_start(hbox5, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

    def  letterfilter(self, letter):
        print("letterfilter", letter)
        self.label.set_text(letter)

tw = pgtestwin()

#print("test")

Gtk.main()

# EOF
