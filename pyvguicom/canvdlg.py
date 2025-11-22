#!/usr/bin/env python3

import gi; gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango
from gi.repository import cairo

import pggui
import pgtests

def textdlg(oldtext = "", parent = None):

    #warnings.simplefilter("ignore")

    #print("textdlg()", oldtext)

    #Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,

    dialog = Gtk.Dialog(title="Get text", modal = True)
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                            Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    if parent:
        dialog.set_transient_for(parent)

    # Spacers
    label1 = Gtk.Label(label="   ");  label2 = Gtk.Label(label="   ")
    label3 = Gtk.Label(label="   ");  label4 = Gtk.Label(label="   ")
    label5 = Gtk.Label(label="   ");  label6 = Gtk.Label(label="   ")
    label7 = Gtk.Label(label="   ");  label8 = Gtk.Label(label="   ")

    #warnings.simplefilter("ignore")
    entry = Gtk.Entry();
    entry.set_text(oldtext)
    #warnings.simplefilter("default")

    entry.set_activates_default(True)

    #if  self2.oldgoto == "":
    #    self2.oldgoto = pedconfig.conf.sql.get_str("goto")
    #    if  self2.oldgoto == None:
    #        self2.oldgoto = ""
    #
    #entry.set_text(self2.oldgoto)

    entry.set_width_chars(24)
    dialog.vbox.pack_start(label4, 0, 0, 0)

    hbox2 = Gtk.HBox()
    hbox2.pack_start(label6, 0, 0, 0)
    hbox2.pack_start(entry, 0, 0, 0)
    hbox2.pack_start(label7, 0, 0, 0)
    dialog.vbox.pack_start(hbox2, 0, 0, 0)
    dialog.vbox.pack_start(label5, 0, 0, 0)

    hbox = Gtk.HBox()
    dialog.vbox.pack_start(hbox, 0, 0, 0)
    dialog.vbox.pack_start(label8, 0, 0, 0)

    dialog.show_all()
    response = dialog.run()
    gotxt = entry.get_text()
    dialog.destroy()
    #warnings.simplefilter("default")

    #if response != Gtk.ResponseType.ACCEPT:
    #    gotxt = ""

    return (response, gotxt)

def canv_colsel(oldcol, title):

    csd = Gtk.ColorSelectionDialog(title)
    col = csd.get_color_selection()
    #col.set_current_color(pggui.float2col(oldcol))
    response = csd.run()
    color = 0
    if response == Gtk.ResponseType.OK:
        color = col.get_current_color()
        #print ("color", color)
    csd.destroy()
    return pggui.col2float(color)

def propdlg(objectx, parent = None):

    print("propdlg()", objectx)

    dialog = Gtk.Dialog(title="Object Properties", modal = True)
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                            Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    if parent:
        dialog.set_transient_for(parent)

    # Spacers
    label1 = Gtk.Label(label="   ");  label2 = Gtk.Label(label="   ")

    dialog.show_all()
    response = dialog.run()
    #gotxt = entry.get_text()
    dialog.destroy()


# EOF

