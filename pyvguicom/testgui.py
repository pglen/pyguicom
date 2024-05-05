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

import pggui

def timer(ledx):
    # Reset LED
    ledx.set_color(ledx.orgcolor) #"#ffffff")
    pass

if __name__ == "__main__":

    w = Gtk.Window()
    w.set_size_request(400, 300)
    w.connect("destroy", Gtk.main_quit)

    vbox = Gtk.VBox();    hbox = Gtk.HBox()

    lab1=Gtk.Label(label="Test\nText\n Here\n")
    hbox.pack_start(lab1, 1, 1, 0)
    vbox.pack_start(hbox, 1, 1, 0)

    arr = [("111 ", "222 "),  ("333 ", "444")]
    tt = pggui.TextTable(arr)

    hbox4b = Gtk.HBox()
    hbox4b.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    hbox4b.pack_start(tt, 0, 0, 0)
    hbox4b.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    vbox.pack_start(hbox4b, 0, 0, 2)

    #tr = pggui.TextRow("aa", "bb", w)
    #vbox.pack_start(tr, 0, 0, 2)

    def _callb(arg2, arg3 = 0, arg4 = 0):
        print("callb", arg2, arg3, arg4)
        lab1.set_text("callb \n" + str(arg2)[:24] \
                    + "\n" + str(arg3)[:24] + "\n" + str(arg4)[:24])
        led.set_color("#ff0000")
        GLib.timeout_add(300, timer, led)

    logo = pggui.Logo("Logo", font="Dejavu 32")
    vbox.pack_start(logo, 0, 0, 2)

    hbox4a = Gtk.HBox()
    wb = pggui.WideButt("Wide Button", _callb, 24)
    hbox4a.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    hbox4a.pack_start(wb, 0, 0, 0)
    hbox4a.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    vbox.pack_start(hbox4a, 0, 0, 2)

    lb = pggui.LabelButt("Label Button", _callb, None)
    vbox.pack_start(lb, 0, 0, 2)

    la = pggui.Label("Label", font="italic")
    vbox.pack_start(la, 0, 0, 2)

    ft = pggui.FrameTextView()
    for aa in range(10):
        ft.append("Hello %d\n" % aa)

    vbox.pack_start(ft, 0, 0, 2)

    marr = ["First Menu Item","Second Menu Item","Third Menu Item",
            "Fourth Menu Item",  ]

    hbox3 = Gtk.HBox()
    mb = pggui.MenuButt(marr, _callb, None)
    hbox3.pack_start(mb, 0, 0, 0)

    hbox3.pack_start(Gtk.Label(label="  Menu Button "), 0, 0, 0)
    hbox3.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    led = pggui.Led("#fffffff")
    hbox3.pack_start(led, 0, 0, 0)
    hbox3.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    #hbox3.pack_start(led, 1, 1, 0)
    vbox.pack_start(hbox3, 0, 0, 2)

    #hbox4 = Gtk.HBox()
    #hbox4.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    #hbox4.pack_start(led, 0, 0, 0)
    #hbox4.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    #vbox.pack_start(hbox4, 0, 0, 2)

    rarr = ["One", "Two", "Three", "Four", "Five"]
    rg = pggui.RadioGroup(rarr, _callb, True)
    vbox.pack_start(rg, 0, 0, 2)

    hbox5 = Gtk.HBox()
    cb = pggui.ComboBox(marr, _callb)
    hbox5.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    hbox5.pack_start(cb, 0, 0, 2)
    hbox5.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    vbox.pack_start(hbox5, 0, 0, 2)

    hbox6 = Gtk.HBox()
    sp = pggui.Spinner(cb=_callb)
    hbox6.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    hbox6.pack_start(sp, 0, 0, 2)
    hbox6.pack_start(Gtk.Label(label="  "), 1, 1, 0)
    vbox.pack_start(hbox6, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("E_xit")
    butt.connect("clicked", Gtk.main_quit)
    vbox.pack_start(butt, 0, 0, 2)

    w.add(vbox)
    w.show_all()
    w.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
    Gtk.main()

# EOF
