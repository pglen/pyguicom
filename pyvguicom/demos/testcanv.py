#!/usr/bin/python

# pylint: disable=C0103
# pylint: disable=C0209
# pylint: disable=C0321
# pylint: disable=C0410
# pylint: disable=C0413

import sys
#import string, random, datetime

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

sys.path.append(".")

import pgcanv
import pgdlgs
import pgbutt
import canvdlg
import comparse

canv = None

__doc__ = ''' Test for canvas '''

def tbc(arg1, arg2):
    ''' Doc String '''
    print("Toolbox:", arg1.text, "cnt =", arg2)

def callb(arg1):
    ''' Doc String '''

    if arg1.cnt == 0:
        #print("New")
        canv.save()
        canv.coll = []
    if arg1.cnt == 1:
        #print("Load")
        canv.open()
    if arg1.cnt == 2:
        #print("Save")
        canv.save()
    if arg1.cnt == 3:
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
    ''' Doc String '''

    global canv

    w = Gtk.Window()
    w.set_size_request(800, 600)
    w.set_position(Gtk.WindowPosition.CENTER)
    w.config = conf
    w.connect("destroy", Gtk.main_quit)
    try:
        w.set_icon_from_file("images/canv.png")
    except:
        #print(sys.exc_info())
        pass

    vbox = Gtk.VBox()
    hbox = Gtk.HBox()

    hbox.pack_start(canvdlg.ToolBox(tbc, w), 0, 0, 0)
    vbox.pack_start(hbox, 0, 0, 0)

    canv = pgcanv.Canvas(w, config=config)
    vbox.pack_start(canv, 1, 1, 0)

    #statcall = canvdlg.StatusBar(w, "Idle.")
    #vbox.pack_start(statcall, 0, 0, 0)
    #canv.statcall = statcall

    buttarr = ["  _New  ", "  Op_en  ", "  _Save  ", "  E_xit  "]
    estrip = pgbutt.ExitStrip(buttarr, callb)
    vbox.pack_start(estrip, 0, 0, 0)

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

    config = comparse.parse(sys.argv, optx)
    if config.verbose > 2:
        print(config)
    mainfunc(config)

# EOF
