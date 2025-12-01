#!/usr/bin/env python3

import math, warnings

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
import pgentry

def textdlg(oldtext = "", parent = None):

    #print("textdlg()", oldtext)
    dialog = Gtk.Dialog(title="Get text", modal = True)
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                            Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
    dialog.set_default_response(Gtk.ResponseType.ACCEPT)

    dialog.set_default_size(640, 480)

    if parent:
        dialog.set_transient_for(parent)

    # Spacers
    label1 = Gtk.Label(label="   ");  label2 = Gtk.Label(label="   ")
    label3 = Gtk.Label(label="   ");  label4 = Gtk.Label(label="   ")
    label5 = Gtk.Label(label="   ");  label6 = Gtk.Label(label="   ")
    label7 = Gtk.Label(label="   ");  label8 = Gtk.Label(label="   ")

    #warnings.simplefilter("ignore")
    #entry = Gtk.Entry();
    headx, cont = pgentry.wrap(pgentry.TextViewx())
    cont.set_text(oldtext)
    #warnings.simplefilter("default")
    #entry.set_activates_default(True)
    #entry.set_width_chars(24)
    #dialog.vbox.pack_start(label4, 0, 0, 0)

    hbox2 = Gtk.HBox()
    hbox2.pack_start(label6, 0, 0, 0)
    hbox2.pack_start(headx, 1, 1, 0)
    hbox2.pack_start(label7, 0, 0, 0)
    dialog.vbox.pack_start(hbox2, 1, 1, 0)
    dialog.vbox.pack_start(label5, 0, 0, 0)

    #hbox = Gtk.HBox()
    #dialog.vbox.pack_start(hbox, 0, 0, 0)
    #dialog.vbox.pack_start(label8, 0, 0, 0)

    dialog.show_all()
    response = dialog.run()
    gotxt = cont.get_text()
    dialog.destroy()
    #warnings.simplefilter("default")

    #if response != Gtk.ResponseType.ACCEPT:
    #    gotxt = ""

    return (response, gotxt)

def canv_colsel(oldcol, title):

    #print ("oldcol", oldcol)
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

    def add(self, widg, width = 1, options=Gtk.AttachOptions.EXPAND):
        warnings.simplefilter("ignore")
        self.attach(widg, self.col, self.col + width, self.row,
                self.row + width, options, options, width, width);
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
                    ("*.*", "ALL files (*.*)"),
                    ("*.png", "PNG Image files (*.png)"),
                    ("*.jpg", "JPG Image files (*.jpg)"),
                    #("*.jpeg", "JPEG Image files (*.jpeg)"),
                  ]
        fff = pgdlgs.opendialog(filter=filter)
        if not fff:
            return
        #print("imgok", fff)
        texts[2].set_text(fff)
        objectx[0].image = fff
        parent.queue_draw()

    def fontok(arg):
        fff = pgdlgs.fontdialog(parent=dialog,
                        family=objectx[0].fontstr, fsize=objectx[0].fsize)
        #print("fontok", fff)
        if fff:
            objectx[0].skipsize = True
            objectx[0].fontstr = fff[0] + " " + fff[1] + " " + str(fff[2])
            objectx[0].fsize = fff[2]
            parent.queue_draw()

    for aa in range(len(labels)):
        texts.append(Gtk.Entry())
        dtab.add(pggui.Label(labels[row]))
        dtab.add(texts[row])
        if aa == 0 and objectx[0].type == "Text":
            bbutt = pgbutt.smallbutt("Select Font", fontok)
            dtab.add(bbutt)
        if aa == 2 and objectx[0].type == "Image":
            bbutt = pgbutt.smallbutt("Browse Image", imgok)
            dtab.add(bbutt)
        dtab.newrow()
        row += 1

    texts[0].set_text(objectx[0].text)
    texts[1].set_text(objectx[0].tooltip)

    if objectx[0].type == "Image":
        texts[2].set_text(objectx[0].image)

    dialog.get_content_area().pack_start(dtab, 0, 0, 4)

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

    hbox2.pack_start(Gtk.Label(label="   "), 1, 1, 4)
    hbox2.pack_start(sb1, 0, 0, 4)
    hbox2.pack_start(sb2, 0, 0, 4)
    hbox2.pack_start(Gtk.Label(label="   "), 1, 1, 4)

    dialog.get_content_area().pack_start(hbox2, 0, 0, 4)

    def callb_rest(sim):
        if objectx[0].arr2:
            objectx[0].arr = objectx[0].arr2
            parent.queue_draw()

    def callb_sim(sim):
        if not objectx[0].arr2:
            objectx[0].arr2 = objectx[0].arr
        arr2 = []
        for cnt, aa in enumerate(objectx[0].arr):
            if cnt %2 == 0:
                arr2.append(aa)
        objectx[0].arr = arr2
        parent.queue_draw()

    def callb_smooth(sim):
        if not objectx[0].arr2:
            objectx[0].arr2 = objectx[0].arr
        lenx = len(objectx[0].arr)
        #print("bounds:", objectx[0].arr[0], objectx[0].arr[lenx-1] )

        if objectx[0].arr[lenx-1][0] == 0:
            rat = objectx[0].arr[0][0] / objectx[0].arr[0][1]
        else:
            rat = objectx[0].arr[lenx-1][0] / objectx[0].arr[lenx-1][1]

        #print("rat", rat)
        arr2 = []
        prev = None
        for aa in objectx[0].arr:
            if not prev:
                prev = aa               # Eat first item
                arr2.append(aa)
                continue
            # Adjust entry to the mean slope
            bb = int(round((aa[0] - prev[0]) * rat))
            arr2.append((aa[0], prev[1] + bb))
            prev = aa
        objectx[0].arr = arr2
        parent.queue_draw()

    if objectx[0].type == "Stroke":
        hbox3 = Gtk.HBox()
        hbox3.pack_start(Gtk.Label(label="   "), 1, 1, 4)
        rest = pgbutt.smallbutt("Restore", callb_rest)
        simp = pgbutt.smallbutt("Simplify", callb_sim)
        smooth = pgbutt.smallbutt("Smooth", callb_smooth)
        hbox3.pack_start(rest, 0, 0, 4)
        hbox3.pack_start(simp, 0, 0, 4)
        hbox3.pack_start(smooth, 0, 0, 4)
        hbox3.pack_start(Gtk.Label(label="   "), 1, 1, 4)
        dialog.get_content_area().pack_start(hbox3, 0, 0, 4)

    dialog.show_all()
    response = dialog.run()
    if response == Gtk.ResponseType.ACCEPT:
        objectx[0].text = texts[0].get_text()
        objectx[0].tooltip = texts[1].get_text()
        if  objectx[0].type == "Image":
            objectx[0].image =  texts[2].get_text()
            objectx[0].loadimg()
    dialog.destroy()

class StatusBar(Gtk.VBox):

    def __init__(self, parent, initial = "Idle"):
        self.tout = 0
        self.parent = parent
        super(StatusBar, self).__init__()
        self.hbox = Gtk.HBox()
        self.idle = initial
        self.text = Gtk.Label(label=initial)
        #self.text.set_justify(Gtk.Justification.LEFT)
        self.text.set_xalign(0)

        self.hbox.pack_start(Gtk.Label(label="  Status:  "), 0, 0, 0)
        self.hbox.pack_start(self.text, 1, 1, 0)
        self.hbox.pack_start(Gtk.Label(label="  "), 0, 0, 0)

        self.add(self.hbox)

    def set_status_text(self, text):
        self.text.set_text(text)
        if self.tout:
            GLib.source_remove(self.tout)
        self.tout = GLib.timeout_add(500 + len(text) * 200, self.idlecall)

    def idlecall(self):
        #print("Idle")
        self.tout = 0
        self.text.set_text(self.idle)

class ToolBox(Gtk.VBox):

    def __init__(self, callb, parent):
        #Gtk.Window.__init__(self, Gtk.WindowType.POPUP)
        #Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)
        #Gtk.Toolbar.__init__(self)
        super(ToolBox, self).__init__()
        self.statcall = None

        #self.set_size_request(10, 10)
        #self.set_default_size(10, 10)
        #self.set_keep_above(True)
        #self.set_decorated(False)

        self.drag = False
        self.dragpos = (0, 0)
        self.callb = callb
        self.opacity = 1

        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button_rel)
        self.connect("motion-notify-event", self.area_motion)

        vbox = Gtk.VBox()

        self.labelm = Gtk.Label(label=" - ")
        self.labelx = Gtk.Label(label=" x ")
        self.toolt = Gtk.Label(label="Main Toolbox")

        self.hboxt = Gtk.HBox()
        self.hboxt.pack_start(self.labelm, 0, 0, 0)
        self.hboxt.pack_start(self.toolt, 1, 1, 0)
        self.hboxt.pack_start(self.labelx, 0, 0, 0)

        self.hbox = Gtk.HBox()
        tarr = ((Gtk.STOCK_OPEN, "Open"), (Gtk.STOCK_SAVE, "Save"),
                    (Gtk.STOCK_COPY, "Copy"), (Gtk.STOCK_PASTE, "Paste"),
                    (Gtk.STOCK_NO, "None"), (Gtk.STOCK_CLEAR, "Clear"),
                    (Gtk.STOCK_DELETE, "Delete"), (Gtk.STOCK_PROPERTIES , "Proerties"),
                     )
        cnt = 0
        for aa in tarr:
            warnings.simplefilter("ignore")
            butt = Gtk.ToolButton().new_from_stock(aa[0])
            warnings.simplefilter("default")
            butt.text = aa[0]
            butt.set_tooltip_text(aa[1])
            butt.connect("clicked", self._callb, cnt)
            cnt += 1
            self.hbox.add(butt)

        self.hbox2 = Gtk.HBox()
        tarr2 = ( (Gtk.STOCK_UNDO, "Undo"), (Gtk.STOCK_REDO, "Redo"),
                    (Gtk.STOCK_COLOR_PICKER, "Color"), (Gtk.STOCK_YES , "yes?"),
                    (Gtk.STOCK_SELECT_ALL , "SelAll"), (Gtk.STOCK_SELECT_FONT , "Font"),
                    (Gtk.STOCK_ZOOM_100 , "Zoom100"), (Gtk.STOCK_ZOOM_FIT , "ZoomFit"),
                     )
        for aa in tarr2:
            warnings.simplefilter("ignore")
            butt = Gtk.ToolButton().new_from_stock(aa[0])
            warnings.simplefilter("default")
            butt.text = aa[0]
            butt.set_tooltip_text(aa[1])
            butt.connect("clicked", self._callb, cnt)
            cnt += 1
            #self.hbox2.add(butt)
            self.hbox.add(butt)

        #vbox.add(self.hboxt)
        vbox.add(self.hbox)
        #vbox.add(self.hbox2)
        self.add(vbox)

    def callb2(self, arg1, arg2):
        ''' Internal callback '''
        print("callb2", arg1, arg2)

    def _callb(self, arg1, arg2):
        ret = False
        if self.callb:
            ret = self.callb(arg1, arg2)

        # If no external, or external returned False
        if not ret:
            self.callb2(arg1, arg2)

    def area_motion(self, area, event):
        #print ("motion event", event.state, event.x, event.y)
        if self.drag:
            #print ("drag toolbox", event.state, event.x, event.y)
            #print("delta:", event.x - self.dragpos[0],  event.y - self.dragpos[1])
            self.changed = True
            pos = self.get_position()
            self.move(pos[0] + event.x - self.dragpos[0],
                pos[1] + event.y - self.dragpos[1])

    def area_button_rel(self, area, event):
        self.drag = False

    def area_button(self, area, event):

        #return
        #print("moudown", event.x, event.y)
        hit = pggui.Rectangle(event.x, event.y, 2, 2)

        rr = self.labelm.get_allocation()
        rrr = pggui.Rectangle(rr.x, rr.y, rr.width, rr.height)
        if rrr.intersect(hit)[0]:
            #print("objl", rr.x, rr.y)
            if self.opacity == 1:
                self.opacity = 0.5
            else:
                self.opacity = 1
            self.set_opacity(self.opacity)

        rr = self.toolt.get_allocation()
        rrr = pggui.Rectangle(rr.x, rr.y, rr.width, rr.height)
        if rrr.intersect(hit)[0]:
            #print("objhead", rr.x, rr.y)
            self.dragpos = event.x, event.y
            self.drag = True

        rr = self.labelx.get_allocation()
        rrr = pggui.Rectangle(rr.x, rr.y, rr.width, rr.height)
        if rrr.intersect(hit)[0]:
            print("objx", rr.x, rr.y)
            self.hide()
        return True

    def show_box(self, parent):
        self.parent = parent
        self.set_transient_for (self.parent)
        #self.set_parent(parent)
        sxx, syy = self.parent.get_position()
        self.move(sxx + 30, syy + 180)
        self.show_all()

# EOF
