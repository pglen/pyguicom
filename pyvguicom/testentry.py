#!/usr/bin/env python3

from __future__ import print_function

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

import pgentry
import pgutils
import pggui

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


        gridx = Gtk.Grid()
        gridx.set_column_spacing(6)
        gridx.set_row_spacing(6)

        vbox  = Gtk.VBox()

        rowcnt = 0
        self.dat_dict = {}
        sumx = Gtk.HBox()
        buttx2 = Gtk.Button.new_with_mnemonic("Sele_ct Date")
        tp1 =("Full Nam_e: ", "name", "Enter full name (TAB to advance)", None)
        tp2 = ("Date o_f birth: ", "dob", "Date of birth, YYYY/MM/DD", None)
        lab1, lab2 = pgentry.gridquad(gridx, rowcnt, 0, tp1, tp2, buttx2)
        #buttx2.connect("clicked", self.pressed_dob, lab2)
        self.dat_dict['name'] = lab1
        self.dat_dict['dob'] = lab2
        rowcnt += 1

        #gridx.attach(pggui.vspacer(8), 0, rowcnt, 1, 1)

        tp3 = ("Location of birth: ", "lob", "Location: City / Country", None)
        tp4 = ("Nick Name: ", "nick", "Enter nick name / Alias if available", None)
        lab3, lab4 = pgentry.gridquad(gridx, 0, rowcnt, tp3, tp4)
        lab2.set_gray(True)
        self.dat_dict['lob'] = lab3
        self.dat_dict['nick'] = lab4
        rowcnt += 1

        tp5 = ("Long entr_y ", "nick", "Test Long entry", None)
        lab5 = pgentry.griddouble(gridx, 0, rowcnt, tp5)
        self.dat_dict['lob'] = lab5
        rowcnt += 1

        tp6 = ("Long entr_y (read only)", "nick", "Test Long entry", None)
        lab6 = pgentry.griddouble(gridx, 0, rowcnt, tp6)
        lab6.set_gray(True)
        self.dat_dict['lob'] = lab6
        rowcnt += 1

        tp6x = ("Note_s: ", "", "Text for Notes. Press Shift Enter to advance Tab", None)
        lab6x = pgentry.gridsingle(gridx, 0, rowcnt, tp6x)
        self.dat_dict['notes'] = lab6x
        rowcnt += 1

        #gridx.attach(pggui.vspacer(8), 0, rowcnt, 1, 1)
        #rowcnt += 1

        hbox2 = Gtk.HBox()
        hbox2.pack_start(gridx, 1, 1, 2)

        vbox.pack_start(hbox2, 0, 0, 2)

        #hbox5 = Gtk.HBox()
        #self.label = Gtk.Label.new("Test strings here")
        #hbox5.pack_start(self.label, 1, 1, 2)
        #vbox.pack_start(hbox5, 0, 0, 2)

        butt = Gtk.Button.new_with_mnemonic("E_xit")
        butt.connect("clicked", Gtk.main_quit)
        vbox.pack_start(butt, 0, 0, 2)

        self.add(vbox)
        self.show_all()

tw = pgtestwin()
#print("test")
Gtk.main()

# EOF
