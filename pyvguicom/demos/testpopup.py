#!/usr/bin/env python

import sys, random, time, warnings

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

from pyvguicom import pgutils

import pgbutt
import pggui
import pgtests

warnings.simplefilter("default")

class testWin(Gtk.Window):

    def __init__(self, *args, **kwargs):

        super(testWin, self).__init__(*args, **kwargs)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(640, 480)

        self.connect("destroy", self.exit_prog)
        vbox13 = Gtk.VBox()
        vbox13.pack_start(Gtk.Label.new("  Test sub window implementation  "), 1, 1, 0)

        #popo = Gtk.Popover()
        #vbox13.pack_start(popo, 1, 1, 0)

        self.base = pgbutt.PopBase(self)

        vbox13.pack_start(pggui.ySpacer(), 1, 1, 0)
        hbox14 = Gtk.HBox()
        hbox14.pack_start(pggui.ySpacer(), 1, 1, 0)

        butt3t = pgbutt.smallbutt("T_est", self.testone)
        hbox14.pack_start(butt3t, 0, 0, 0)

        hbox14.pack_start(pggui.ySpacer(), 1, 1, 0)

        butt3y = pgbutt.smallbutt("E_xit", self.exit_prog, "Exit program")
        hbox14.pack_start(butt3y, 0, 0, 0)
        hbox14.pack_start(pggui.ySpacer(), 1, 1, 0)

        vbox13.pack_start(hbox14, 0, 0, 0)
        vbox13.pack_start(pggui.ySpacer(12), 0, 0, 0)

        self.add(vbox13)
        self.show_all()
        self.testone(0)

    def testone(self, arg1):
        self.base.cnt = 0
        GLib.timeout_add(300, self.popone)

    def popone(self):
        sss = "%d " % self.base.cnt + pgtests.randstrrand(26, 148)
        #sss = "Hello %d" % self.base.cnt
        self.base.submit(sss, len(sss) * 300)
        if self.base.cnt < 15:
            return True

    def exit_prog(self, arg):
        print("exit butt", arg)
        self.destroy()
        Gtk.main_quit()

if __name__ == "__main__":
    #Gtk.init(sys.argv)
    testwin = testWin()
    Gtk.main()

# EOF