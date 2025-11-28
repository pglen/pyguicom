#!/usr/bin/env python3

import warnings

import gi; gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango
from gi.repository import cairo

import pggui
import pgbutt
import pgtests
import pgdlgs

def textdlg(oldtext = "", parent = None):

    #print("textdlg()", oldtext)
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

    print ("oldcol", oldcol)
    csd = Gtk.ColorSelectionDialog(title=title)
    col = csd.get_color_selection()
    warnings.simplefilter("ignore")
    col.set_current_color(pggui.float2col(oldcol))
    warnings.simplefilter("default")
    response = csd.run()
    color = oldcol
    csd.destroy()
    if response == Gtk.ResponseType.OK:
        warnings.simplefilter("ignore")
        color = col.get_current_color()
        warnings.simplefilter("default")
        col = pggui.col2float(color)
    else:
        col = oldcol
    #print ("new color", col)
    return col

class   Tablex(Gtk.Table):

    def __init__(self):
        super(Tablex, self).__init__()
        warnings.simplefilter("ignore")
        self.set_col_spacings(4); self.set_row_spacings(4)
        warnings.simplefilter("default")
        self.col = 0; self.row = 0

    def add(self, widg, width = 1):
        warnings.simplefilter("ignore")
        self.attach(widg, self.col, self.col + width, self.row,
                self.row + width, Gtk.AttachOptions.FILL,
                    Gtk.AttachOptions.FILL, width, width);
        warnings.simplefilter("default")
        self.col += 1

    def newrow(self):
        self.row += 1 ; self.col = 0

def propdlg(objectx, parent = None):

    #print("propdlg()", objectx[0].dump())

    dialog = Gtk.Dialog(title="Object Properties", modal = True)
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                            Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    if parent:
        dialog.set_transient_for(parent)

    # Spacers
    label1 = Gtk.Label(label=objectx[0].type);
    dialog.get_content_area().pack_start(label1, 0, 0, 4)

    row = 0
    dtab = Tablex();
    texts = []
    labels = ["Text", "Tooltip"]
    if  objectx[0].type == "Image":
        labels.append("Image")

    def imgok(arg):
        filter =  [
                    ("*.png", "PNG Image files (*.png)"),
                    ("*.jpg", "JPG Image files (*.jpg)"),
                    ("*.jpeg", "JPEG Image files (*.jpeg)"),
                    ("*.*", "ALL files (*.*)"),
                  ]
        fff = pgdlgs.opendialog(filter=filter)
        if not fff:
            return
        print("imgok", fff)
        texts[0].set_text(fff)

    def fontok(arg):
        fff = pgdlgs.fontdialog()
        print("fontok", fff)

    for aa in range(len(labels)):
        texts.append(Gtk.Entry())
        dtab.add(pggui.Label(labels[row]))
        dtab.add(texts[row])
        if aa == 0 and objectx[0].type == "Text":
            bbutt = pgbutt.smallbutt("Select Font", fontok)
            dtab.add(bbutt)
        if aa == 2 and objectx[0].type == "Image":
            bbutt = pgbutt.smallbutt("Browse Image", imgok, font="Arial 20")
            dtab.add(bbutt)
        dtab.newrow()
        row += 1

    texts[0].set_text(objectx[0].text)
    texts[1].set_text(objectx[0].tooltip)

    if  objectx[0].type == "Image":
        texts[2].set_text(objectx[0].image)

    def callb(arg1):
        if arg1.cnt == 1:
            col2 = canv_colsel(objectx[0].col2, "FG Color")
            for aa in objectx:
                if aa.selected:
                    aa.col2 = col2

        if arg1.cnt == 2:
            col1 = canv_colsel(objectx[0].col1, "BG Color")
            for aa in objectx:
                if aa.selected:
                    aa.col1 = col1

    hbox2 = Gtk.HBox()
    sb1 = pgbutt.smallbutt("Foreground Color", callb)
    sb1.cnt = 1
    sb2 = pgbutt.smallbutt("Background Color", callb)
    sb2.cnt = 2

    hbox2.pack_start(sb1, 0, 0, 4)
    hbox2.pack_start(sb2, 0, 0, 4)

    dialog.get_content_area().pack_start(dtab, 0, 0, 4)
    dialog.get_content_area().pack_start(hbox2, 0, 0, 4)

    dialog.show_all()
    response = dialog.run()
    gotxt  = texts[0].get_text()
    gotxt2 = texts[1].get_text()
    #if  objectx[0].type == "Image":
    #    gotxt3 = texts[2].get_text()
    dialog.destroy()
    if response == Gtk.ResponseType.ACCEPT:
        objectx[0].text = gotxt
        objectx[0].tooltip = gotxt2
        if  objectx[0].type == "Image":
            objectx[0].image = gotxt3
            objectx[0].loadimg()

# EOF

