#!/usr/bin/python

# pylint: disable=C0103
# pylint: disable=C0209
# pylint: disable=C0321

import string, random, datetime

import os, sys, getopt, math

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango

sys.path.append(".")

import pgcanv

'''
    def onsave(self, arg1):
        print("Onsave")
    def onopen(self, arg1):
        print("Onopen")
    def OnExit(self, arg1):
        print("Onexit")
'''

class ExitStrip(Gtk.HBox):

    def __init__(self, callb):

        super(ExitStrip, self).__init__()

        cnt = 0
        loadbutt = Gtk.Button.new_with_mnemonic("   Op_en   ")
        loadbutt.cnt = cnt ; cnt += 1
        self.connect(loadbutt, callb)
        self.pack_start(loadbutt, 0, 0, 0)
        self.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        savebutt = Gtk.Button.new_with_mnemonic("   _Save   ")
        savebutt.cnt = cnt ; cnt += 1
        self.connect(savebutt, callb)
        self.pack_start(savebutt, 0, 0, 0)
        self.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        exitbutt = Gtk.Button.new_with_mnemonic("   E_xit   ")
        exitbutt.cnt = cnt ; cnt += 1
        self.connect(exitbutt, callb)
        self.pack_start(exitbutt, 0, 0, 0)

    def connect(self, butt, callx):
        butt.connect("activate", callx)
        butt.connect("pressed", callx)

def tbc(arg1, arg2):
    print("Toolbox:", arg1.text, "cnt =", arg2)
    pass

def callb(arg1):
    print("ExitStrip:", arg1.cnt)
    if arg1.cnt == 2:
        sys.exit(0)

if __name__ == "__main__":

    w = Gtk.Window()
    w.set_size_request(800, 600)
    w.set_position(Gtk.WindowPosition.CENTER)
    w.connect("destroy", Gtk.main_quit)

    vbox = Gtk.VBox()
    hbox = Gtk.HBox()

    hbox.pack_start(pgcanv.ToolBox(tbc, w), 0, 0, 0)
    vbox.pack_start(hbox, 0, 0, 4)

    canv = pgcanv.Canvas(w)
    vbox.pack_start(canv, 1, 1, 0)

    statcall = pgcanv.StatusBar(w, "Idle.")
    vbox.pack_start(statcall, 0, 0, 0)
    canv.statcall = statcall
    estrip = ExitStrip(callb)
    statcall.hbox.pack_start(estrip, 0, 0, 0)

    w.add(vbox)
    w.show_all()
    Gtk.main()

# EOF
