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

import pgtests, pggui

def subdialog(arg2):

    def pressed(arg2, arg3):
        #print("pressed")
        pggui.message("From sub", parent=arg3)
    def pressed2(arg2, arg3):
        #print("pressed2", arg2, arg3)
        arg3.response(Gtk.ResponseType.OK)
        arg3.destroy()

    dialog = Gtk.Dialog(title="Sub")
    #dialog.set_size_request(200, 100)
    dialog.add_button("OK", Gtk.ResponseType.OK)

    bbb = Gtk.Button.new_with_mnemonic("Message")
    dialog.vbox.pack_start(bbb, 0, 0, 4)
    bbb.connect("pressed", pressed, dialog)
    #buttons=Gtk.ButtonsType.CLOSE)
    bbb = Gtk.Button.new_with_mnemonic("E_xit Sub")
    dialog.vbox.pack_start(bbb, 0, 0, 4)
    bbb.connect("pressed", pressed2, dialog)
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.show_all()
    dialog.run()

def test_message(arg2):
    pggui.message("Hello Message")

def test_message_long(arg2):
    pggui.message("Hello Message\nHere we go, longer str.")

def test_yes_no_cancel(arg2):
    ret = pggui.yes_no_cancel("Test Yes No Cancel Message\n" \
                                "Are you sure?")
    mmm = pggui.resp2str(ret)
    print(mmm)
    lab1.set_text(mmm)

def test_no_yes_cancel(arg2):
    ret = pggui.yes_no_cancel("Test No Yes Cancel Message\n" \
                                "Are you sure?", default="No")
    mmm = pggui.resp2str(ret)
    print(mmm)
    lab1.set_text(mmm)

def test_cancel_no_yes(arg2):
    ret = pggui.yes_no_cancel("Test No Yes Cancel Message\n" \
                                "Are you sure?", default="Cancel")
    mmm = pggui.resp2str(ret)
    print(mmm)
    lab1.set_text(mmm)

def test_yes_no(arg2):
    ret = pggui.yes_no("Test Yes No Message\n" \
                        "Are You sure?")
    mmm = pggui.resp2str(ret)
    print(mmm)
    lab1.set_text(mmm)

def test_no_yes(arg2):
    ret = pggui.yes_no("Test No Yes Message\n" \
                        "Are You sure?", default="No")
    mmm = pggui.resp2str(ret)
    print(mmm)
    lab1.set_text(mmm)

if __name__ == "__main__":

    ww = Gtk.Window()
    #ww.set_size_request(400, 300)
    ww.connect("destroy", Gtk.main_quit)

    vbox = Gtk.VBox()
    hbox = Gtk.HBox()

    global lab1
    lab1 = Gtk.Label(label="Test Label")
    hbox.pack_start(lab1, 1, 1, 4)
    vbox.pack_start(hbox, 1, 1, 4)

    butt = Gtk.Button.new_with_mnemonic("Test M_essage")
    butt.connect("clicked", test_message)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Subdialog  M_essage")
    butt.connect("clicked", subdialog)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test Longer Message")
    butt.connect("clicked", test_message_long)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test Yes _no")
    butt.connect("clicked", test_yes_no)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test No Yes")
    butt.connect("clicked", test_no_yes)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test Yes _no _cancel")
    butt.connect("clicked", test_yes_no_cancel)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test _no Yes _cancel")
    butt.connect("clicked", test_no_yes_cancel)
    vbox.pack_start(butt, 0, 0, 2)

    butt = Gtk.Button.new_with_mnemonic("Test cancel _Yes Nol")
    butt.connect("clicked", test_cancel_no_yes)
    vbox.pack_start(butt, 0, 0, 2)


    butt = Gtk.Button.new_with_mnemonic("E_xit")
    butt.connect("clicked", Gtk.main_quit)
    vbox.pack_start(butt, 0, 0, 2)

    ww.add(vbox)
    ww.show_all()

    #signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


