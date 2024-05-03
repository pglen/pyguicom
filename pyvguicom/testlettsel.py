#!/usr/bin/env python3

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

from pgsel import *
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

        #hbox  = Gtk.HBox();

        vbox  = Gtk.VBox()

        self.selector = LetterNumberSel(self.letterfilter, "Mono 16", " ")
        self.selector.set_tooltip_text("Arrow key to navigate, enter / space key to filter")

        hbox2 = Gtk.HBox();
        hbox2.pack_start(Gtk.Label.new("  "), 0, 0, 2)
        hbox2.pack_start(self.selector , 1, 1, 2)
        hbox2.pack_start(Gtk.Label.new("  "), 0, 0, 2)
        vbox.pack_start(hbox2, 0, 0, 2)

        hbox3 = Gtk.HBox();
        self.num = NumberSel("1 2 3 4 5 6 7 8 9", self.letterfilter, "Mono 16")
        self.num.set_tooltip_text("Arrow key to navigate, enter / space key to filter")
        hbox3.pack_start(Gtk.Label.new("  "), 1, 1, 2)
        hbox3.pack_start(self.num, 0, 0, 2)
        hbox3.pack_start(Gtk.Label.new("  "), 1, 1, 2)
        vbox.pack_start(hbox3, 0, 0, 2)

        hbox4 = Gtk.HBox();
        self.num = HourSel(self.letterfilter)
        self.num.set_tooltip_text("Arrow key to navigate, enter / space key to filter")
        hbox4.pack_start(Gtk.Label.new("  "), 1, 1, 2)
        hbox4.pack_start(self.num, 0, 0, 2)
        hbox4.pack_start(Gtk.Label.new("  "), 1, 1, 2)
        vbox.pack_start(hbox4, 0, 0, 2)

        hbox4a = Gtk.HBox();
        self.minx = MinSel(self.letterfilter)
        self.minx.set_tooltip_text("Arrow key to navigate, enter / space key to filter")
        hbox4a.pack_start(Gtk.Label.new("  "), 1, 1, 2)
        hbox4a.pack_start(self.minx, 0, 0, 2)
        hbox4a.pack_start(Gtk.Label.new("  "), 1, 1, 2)
        vbox.pack_start(hbox4a, 0, 0, 2)

        #vbox.pack_start(hbox, 1, 1, 2)

        hbox5 = Gtk.HBox()
        self.label = Gtk.Label.new("Test callback strings here.")
        hbox5.pack_start(self.label, 1, 1, 2)
        vbox.pack_start(hbox5, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

    def  letterfilter(self, letter):
        print("letterfilter '%s'" % letter)
        self.label.set_text("Callback: '%s'" % letter)

tw = pgtestwin()

#print("test")

Gtk.main()

# EOF
