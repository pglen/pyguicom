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

import comline
import pgcanv
import pgdlgs

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

    #print("ExitStrip:", arg1.cnt)
    global canv

    if arg1.cnt == 0:
        #print("Load")
        canv.open()
    if arg1.cnt == 1:
        #print("Save")
        canv.save()
    if arg1.cnt == 2:
        #print("Exit")
        if canv.changed:
            ret = pgdlgs.yes_no_cancel("Save File?",
                                title="File changed.", default="Yes")
            if ret == Gtk.ResponseType.YES:
                canv.save()
            elif ret == Gtk.ResponseType.NO:
                pass
            else:
                return
        sys.exit(0)

def mainfunc(conf):

    global canv

    w = Gtk.Window()
    w.set_size_request(800, 600)
    w.set_position(Gtk.WindowPosition.CENTER)
    w.connect("destroy", Gtk.main_quit)
    try:
        w.set_icon_from_file("images/canv.png")
    except:
        #print(sys.exc_info())
        pass

    vbox = Gtk.VBox()
    hbox = Gtk.HBox()

    hbox.pack_start(pgcanv.ToolBox(tbc, w), 0, 0, 0)
    vbox.pack_start(hbox, 0, 0, 4)

    canv = pgcanv.Canvas(w, config=config)
    vbox.pack_start(canv, 1, 1, 0)

    statcall = pgcanv.StatusBar(w, "Idle.")
    vbox.pack_start(statcall, 0, 0, 0)
    canv.statcall = statcall
    estrip = ExitStrip(callb)
    statcall.hbox.pack_start(estrip, 0, 0, 0)

    if config.xargs:
        #print("Loading:", config.xargs[0])
        canv.readfile(config.xargs[0])
        canv.fname = config.xargs[0]

    w.add(vbox)
    w.show_all()
    Gtk.main()

optx =  \
[  # option - longname - action - type - defval - help
  ("d", "debug",     "=",    int,   0,   "Debug level (0-9) default=0", ),
  ("f", "fname",     "=",    str,   "untitled", "Filename for out data. defval: untitled"),
  ("t", "trace",     "=",    str,   "None", "Trace flag string.",),
  ("v", "verbose",   "+",    int,   0,   "Increase verbosity level.",),
  ("V", "version",   "b",    bool,  False,   "Show version.",),
]

if __name__ == '__main__':

    import comparse
    config = comparse.parse(sys.argv, optx)
    if config.verbose > 2:
        print(config)
    mainfunc(config)

# EOF
