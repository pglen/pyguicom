#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import signal, os, time, sys, pickle, subprocess, random
import math, copy

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Pango

gui_testmode = 0

'''
for a in (style.base, style.fg, style.bg,
      style.light, style.dark, style.mid,
      style.text, style.base, style.text_aa):
for st in (gtk.STATE_NORMAL, gtk.STATE_INSENSITIVE,
           gtk.STATE_PRELIGHT, gtk.STATE_SELECTED,
           gtk.STATE_ACTIVE):
    a[st] = gtk.gdk.Color(0, 34251, 0)
'''


# ------------------------------------------------------------------------
# Bemd some of the parameters for us

class CairoHelper():

    def __init__(self, cr):
        self.cr = cr

    def set_source_rgb(self, col):
        self.cr.set_source_rgb(col[0], col[1], col[2])

    def rectangle(self, rect):
        self.cr.rectangle(rect[0], rect[1], rect[2], rect[3])

    # --------------------------------------------------------------------
    #   0 1           0+2
    #   x,y     -      rr
    #         -   -
    #  midy -       -
    #         -   -
    #           -      bb
    #          midx    1+3

    def romb(self, rect):

        #print("romb", rect[0], rect[1], rect[2], rect[3])
        midx =  rect[0] + rect[2] // 2
        midy =  rect[1] + rect[3] // 2

        self.cr.move_to(rect[0], midy)
        self.cr.line_to(midx, rect[1])
        self.cr.line_to(rect[0]+rect[2], midy)
        self.cr.line_to(midx, rect[1]+rect[3])
        self.cr.line_to(rect[0], midy)

    def circle(self, xx, yy, size):
        self.cr.arc(xx, yy, size, 0,  2 * math.pi)

class   TextTable(Gtk.Table):

    def __init__(self, confarr, main = None, textwidth = 24):
        GObject.GObject.__init__(self)
        self.texts = []
        #self.set_homogeneous(False)
        self.main = main
        row = 0
        for aa, bb in confarr:
            #print("aa", aa, "bb", bb)
            label = Gtk.Label()
            label.set_text_with_mnemonic(aa)
            tbox = Gtk.Entry()
            label.set_mnemonic_widget(tbox)
            tbox.set_width_chars (textwidth)
            self.texts.append(tbox)
            self.attach_defaults(label, 0, 1, row, row + 1)
            self.attach_defaults(tbox,  1, 2, row, row + 1)
            row += 1

class   TextRow(Gtk.HBox):

    def __init__(self, labelx, initval, main, align=20):

        GObject.GObject.__init__(self)
        #super().__init__(self)

        self.set_homogeneous(False)
        self.main = main
        self.label = Gtk.Label()
        self.label.set_text_with_mnemonic(labelx)
        #self.label.set_xalign(1)

        # Adjust for false character
        lenx = len(labelx);
        if "_" in labelx: lenx -= 1
        #spp = int((align - lenx) * 1.8) # Space is smaller than avarage char
        #self.pack_start(Spacer(spp), False, False, 0)

        self.pack_start(Spacer(), False, False, 0)
        self.pack_start(self.label, False, False, 0)
        self.pack_start(Spacer(4), False, False, 0)
        self.tbox = Gtk.Entry()
        self.tbox.set_width_chars (8)
        self.tbox.set_text(initval)
        self.pack_start(self.tbox, False, False, 0)

        self.label.set_mnemonic_widget(self.tbox)

        self.tbox.connect("focus_out_event", self.edit_done)
        self.tbox.connect("key-press-event", self.edit_key)
        self.tbox.connect("key-release-event", self.edit_key_rel)

    def edit_done(self, textbox, event):
        #print(textbox.get_text())
        pass

    def edit_key_rel(self, textbox, event):
        #print(textbox, event.string, event.keyval)
        if event.string == "\t":
            #print("Tab")
            return None

        if event.string == "\r":
            #print("Newline", event.string)
            # Switch to next control
            '''
            #ee = event.copy() #Gdk.Event(Gdk.EventType.KEY_PRESS)
            #ee.keyval = Gdk.KEY_Tab
            #ee.string = "\t"
            #e.state = event.state
            #super().emit("key-release-event", ee)
            #super().foreach(self.callb)
            '''
            pass


    def callb(self, arg1):
        #print ("callb arg1", arg1)
        pass

    def edit_key(self, textbox, event):
        #print(textbox, event.string, event.keyval)
        if event.string == "\t":
            #print("Tab")
            pass
        if event.string == "\r":
            #print("Newline")
            # Switch to next control (any way you can)
            arrx = (Gtk.DirectionType.TAB_FORWARD,  Gtk.DirectionType.RIGHT,
            Gtk.DirectionType.LEFT, Gtk.DirectionType.UP)
            for aa in arrx:
                ret = self.main.child_focus(aa)
                if ret:
                    break

    def get_text(self):
        return self.tbox.get_text()

    def set_text(self, txt):
        return self.tbox.set_text(txt)

# ------------------------------------------------------------------------

class   RadioGroup(Gtk.Frame):

    def __init__(self, rad_arr, call_me):

        GObject.GObject.__init__(self)
        self.buttons = []
        self.callme = call_me
        vbox6 = Gtk.VBox(); vbox6.set_spacing(4);
        vbox6.set_border_width(6)

        if gui_testmode:
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#778888"))

        self.radio = Gtk.RadioButton.new_with_mnemonic(None, "None")

        for aa in range(len(rad_arr)):
            #rad2 = Gtk.RadioButton.new_from_widget(self.radio)
            #rad2.set_label(rad_arr[aa])
            rad2 = Gtk.RadioButton.new_with_mnemonic_from_widget(self.radio, rad_arr[aa])
            self.buttons.append(rad2)
            rad2.connect("toggled", self.radio_toggle, aa)
            vbox6.pack_start(rad2, False, False, False)

        self.add(vbox6)

    def radio_toggle(self, button, idx):
        #print("RadioGroup", button.get_active(), "'" + str(idx) + "'")
        if  button.get_active():
            self.callme(button, self.buttons[idx].get_label())

    def set_tooltip(self, idx, strx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_tooltip_text(strx)

    def set_entry(self, idx, strx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_label(strx)

    def set_sensitive(self, idx, valx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_sensitive(valx)

    def get_size(self):
        return len (self.buttons)

    def set_check(self, idx, valx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_active(valx)
        self.buttons[idx].toggled()

    def get_check(self):
        cnt = 0
        for aa in (self.buttons):
            if aa.get_active():
                return cnt
            cnt += 1
        # Nothing selected ...
        return -1

    def get_text(self):
        for aa in (self.buttons):
            if aa.get_active():
                return aa.get_label()
        # Nothing selected ... empty str
        return ""

class Led(Gtk.DrawingArea):

    def __init__(self, color, size = 20, border = 2):
        GObject.GObject.__init__(self)
        #self.size_allocate();
        #self.size_request()
        self.border = border
        self.set_size_request(size + border, size + border)
        self.connect("draw", self.draw)
        self.color =  color

    def set_color(self, col):
        self.color = col
        self.queue_draw()

    def draw(self, area, cr):
        rect = self.get_allocation()
        #print ("draw", rect)

        #cr.rectangle(0, 0, rect.width, rect.height);
        #x = 0; y = 0; width = 10; height = 10
        #cr.save()
        #cr.translate(x + width / 2., y + height / 2.)
        #cr.scale(width / 2., height / 2.)
        #cr.restore()

        ccc = str2float(self.color)
        cr.set_source_rgba(ccc[0] * 0.7, ccc[1] * 0.7, ccc[2] * 0.7)
        cr.arc(rect.width/2, rect.height/2., rect.width/2., 0., 2 * math.pi)
        cr.fill()

        cr.set_source_rgba(ccc[0], ccc[1], ccc[2])
        cr.arc(rect.width/2, rect.height/2, rect.width / 2. * .8, 0., 2 * math.pi)
        cr.fill()

        # Reflection on the r
        cr.set_source_rgba(ccc[0], ccc[1] + 0.51, ccc[2])
        cr.arc(rect.width/2+1, rect.height/2, rect.width / 2. * .2, 0., 2 * math.pi)
        cr.fill()


# Bug fix in Gtk

class   SeparatorMenuItem(Gtk.SeparatorMenuItem):

    def __init__(self):
        Gtk.SeparatorMenuItem.__init__(self);
        self.show()

# ------------------------------------------------------------------------

class Menu():

    def __init__(self, menarr, callb, event, submenu = False):

        #GObject.GObject.__init__(self)

        self.callb = callb
        self.menarr = menarr
        self.gtkmenu = Gtk.Menu()
        self.title = menarr[0]

        cnt = 0
        for aa in self.menarr:
            #print("type aa", type(aa))
            if type(aa) == str:
                if aa == "-":
                    mmm = SeparatorMenuItem()
                else:
                    mmm = self._create_menuitem(aa, self.menu_fired, cnt)

                if not submenu:
                    self.gtkmenu.append(mmm)
                    if cnt == 0:
                        mmm.set_sensitive(False)
                        self.gtkmenu.append(SeparatorMenuItem())
                else:
                    if cnt != 0:
                        self.gtkmenu.append(mmm)

            elif type(aa) == Menu:
                mmm = self._create_menuitem(aa.title, self.dummy, cnt)
                mmm.set_submenu(aa.gtkmenu)
                self.gtkmenu.append(mmm)
            else:
                raise ValueError("Menu needs text or submenu")
            cnt = cnt + 1

        if not submenu:
            self.gtkmenu.popup(None, None, None, None, event.button, event.time)

    def dummy(self, menu, menutext, arg):
        pass

    def _create_menuitem(self, string, action, arg = None):
        rclick_menu = Gtk.MenuItem(string)
        rclick_menu.connect("activate", action, string, arg);
        rclick_menu.show()
        return rclick_menu

    def menu_fired(self, menu, menutext, arg):
        #print ("menu item fired:", menutext, arg)
        if self.callb:
            self.callb(menutext, arg)
        self.gtkmenu = None

class MenuButt(Gtk.DrawingArea):

    def __init__(self, menarr, callb, tooltip = "Menu", size = 20, border = 2):
        GObject.GObject.__init__(self)
        self.border = border
        self.callb = callb
        self.menarr = menarr
        self.set_size_request(size + border, size + border)
        self.connect("draw", self.draw)
        self.connect("button-press-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        self.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.set_tooltip_text(tooltip)
        self.set_can_focus(True)

    def _create_menuitem(self, string, action, arg = None):
        rclick_menu = Gtk.MenuItem(string)
        rclick_menu.connect("activate", action, string, arg);
        rclick_menu.show()
        return rclick_menu

        # Create the menubar and toolbar
        action_group = Gtk.ActionGroup("DocWindowActions")
        action_group.add_actions(entries)
        return action_group

    def area_key(self, area, event):
        pass
        #print("keypress mb", event.type, event.string);

    def area_button(self, area, event):
        #print("menu butt ", event.type, event.button);
        if  event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:
                #print( "Left Click at x=", event.x, "y=", event.y)
                self.grab_focus()
                self.menu3 = Gtk.Menu()
                cnt = 0
                for aa in self.menarr:
                    self.menu3.append(self._create_menuitem(aa, self.menu_fired, cnt))
                    cnt = cnt + 1

                self.menu3.popup(None, None, None, None, event.button, event.time)

    def menu_fired(self, menu, menutext, arg):
        #print ("menu item fired:", menutext, arg)
        if self.callb:
            self.callb(menutext, arg)

    def _draw_line(self, cr, xx, yy, xx2, yy2):
        cr.move_to(xx, yy)
        cr.line_to(xx2, yy2)
        cr.stroke()

    def draw(self, area, cr):
        rect = self.get_allocation()
        #print ("draw", rect)

        if self.is_focus():
            cr.set_line_width(3)
        else:
            cr.set_line_width(2)

        self._draw_line(cr, self.border, rect.height/4,
                                rect.width - self.border, rect.height/4);
        self._draw_line(cr, self.border, 2*rect.height/4,
                                rect.width - self.border, 2*rect.height/4);
        self._draw_line(cr, self.border, 3*rect.height/4,
                                rect.width - self.border, 3*rect.height/4);

# ------------------------------------------------------------------------

class Lights(Gtk.Frame):

    def __init__(self, col_arr, size = 6, call_me = None):

        GObject.GObject.__init__(self)
        self.box_arr = []
        vboxs = Gtk.VBox()
        vboxs.set_spacing(4);
        vboxs.set_border_width(4)

        for aa in col_arr:
            box = self.colbox(str2float(aa), size)
            vboxs.pack_start(box, False, False, False)
            self.box_arr.append(box)

        self.add(vboxs)

    def set_color(self, idx, col):
        if idx >= len(self.box_arr):
            raise ValueError(IDXERR)
        self.box_arr[idx].modify_bg(Gtk.StateFlags.NORMAL, str2col(col))

    def set_colors(self, colarr):
        for idx in range(len(self.box_arr)):
            self.box_arr[idx].modify_bg(
                        Gtk.StateFlags.NORMAL, str2col(colarr[idx]))

    def set_tooltip(self, idx, strx):
        if idx >= len(self.box_arr):
            raise ValueError(IDXERR)
        self.box_arr[idx].set_tooltip_text(strx)

    def set_tooltips(self, strarr):
        for idx in range(len(self.box_arr)):
            self.box_arr[idx].set_tooltip_text(strarr[idx])

    def get_size(self):
        return len (self.box_arr)

    def colbox(self, col, size):

        lab1 = Gtk.Label("  " * size + "\n" * (size // 3))
        lab1.set_lines(size)
        eventbox = Gtk.EventBox()
        frame = Gtk.Frame()
        frame.add(lab1)
        eventbox.add(frame)
        eventbox.color =  col  # Gtk.gdk.Color(col)
        eventbox.modify_bg(Gtk.StateFlags.NORMAL, float2col(eventbox.color))
        return eventbox

class WideButt(Gtk.Button):

    def __init__(self, labelx, callme = None, space = 2):
        #super().__init__(self)
        GObject.GObject.__init__(self)
        self.set_label(" " * space + labelx + " " * space)
        self.set_use_underline (True)
        if callme:
            self.connect("clicked", callme)

class ScrollListBox(Gtk.Frame):

    def __init__(self, limit = -1, colname = '', callme = None):
        Gtk.Frame.__init__(self)
        self.listbox = ListBox(limit, colname)
        if callme:
            self.listbox.set_callback(callme)
        self.listbox.scroll = Gtk.ScrolledWindow()
        self.listbox.scroll.add_with_viewport(self.listbox)
        self.add(self.listbox.scroll)
        self.autoscroll = True

    # Propagate needed ops to list control

    def append_end(self, strx):
        #print("ser str append", strx)
        self.listbox.append(strx)

        if self.autoscroll:
            usleep(10)              # Wait for it to go to screen
            sb = self.listbox.scroll.get_vscrollbar()
            sb.set_value(2000000)
        self.listbox.select(-1)

    def clear(self):
        self.listbox.clear()

    def select(self, num):
        self.listbox.select(num)

class   TextRow(Gtk.HBox):

    def __init__(self, labelx, initval, main, align=20):

        GObject.GObject.__init__(self)
        #super().__init__(self)

        self.set_homogeneous(False)
        self.main = main
        self.label = Gtk.Label()
        self.label.set_text_with_mnemonic(labelx)
        #self.label.set_xalign(1)

        # Adjust for false character
        lenx = len(labelx);
        if "_" in labelx: lenx -= 1
        #spp = int((align - lenx) * 1.8) # Space is smaller than avarage char
        #self.pack_start(Spacer(spp), False, False, 0)

        self.pack_start(Spacer(), False, False, 0)
        self.pack_start(self.label, False, False, 0)
        self.pack_start(Spacer(4), False, False, 0)
        self.tbox = Gtk.Entry()
        self.tbox.set_width_chars (8)
        self.tbox.set_text(initval)
        self.pack_start(self.tbox, False, False, 0)

        self.label.set_mnemonic_widget(self.tbox)

        self.tbox.connect("focus_out_event", self.edit_done)
        self.tbox.connect("key-press-event", self.edit_key)
        self.tbox.connect("key-release-event", self.edit_key_rel)

    def edit_done(self, textbox, event):
        #print(textbox.get_text())
        pass

    def edit_key_rel(self, textbox, event):
        #print(textbox, event.string, event.keyval)
        if event.string == "\t":
            #print("Tab")
            return None

        if event.string == "\r":
            #print("Newline", event.string)
            # Switch to next control
            '''
            #ee = event.copy() #Gdk.Event(Gdk.EventType.KEY_PRESS)
            #ee.keyval = Gdk.KEY_Tab
            #ee.string = "\t"
            #e.state = event.state
            #super().emit("key-release-event", ee)
            #super().foreach(self.callb)
            '''

    def callb(self, arg1):
        #print ("callb arg1", arg1)
        pass

    def edit_key(self, textbox, event):
        #print(textbox, event.string, event.keyval)
        if event.string == "\t":
            #print("Tab")
            pass
        if event.string == "\r":
            #print("Newline")
            # Switch to next control (any way you can)
            arrx = (Gtk.DirectionType.TAB_FORWARD,  Gtk.DirectionType.RIGHT,
            Gtk.DirectionType.LEFT, Gtk.DirectionType.UP)
            for aa in arrx:
                ret = self.main.child_focus(aa)
                if ret:
                    break

    def get_text(self):
        return self.tbox.get_text()

    def set_text(self, txt):
        return self.tbox.set_text(txt)

# ------------------------------------------------------------------------

class   RadioGroup(Gtk.Frame):

    def __init__(self, rad_arr, call_me):

        GObject.GObject.__init__(self)
        self.buttons = []
        self.callme = call_me
        vbox6 = Gtk.VBox(); vbox6.set_spacing(4);
        vbox6.set_border_width(6)

        if gui_testmode:
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#778888"))

        self.radio = Gtk.RadioButton.new_with_mnemonic(None, "None")

        for aa in range(len(rad_arr)):
            #rad2 = Gtk.RadioButton.new_from_widget(self.radio)
            #rad2.set_label(rad_arr[aa])
            rad2 = Gtk.RadioButton.new_with_mnemonic_from_widget(self.radio, rad_arr[aa])
            self.buttons.append(rad2)
            rad2.connect("toggled", self.radio_toggle, aa)
            vbox6.pack_start(rad2, False, False, False)

        self.add(vbox6)

    def radio_toggle(self, button, idx):
        #print("RadioGroup", button.get_active(), "'" + str(idx) + "'")
        if  button.get_active():
            self.callme(button, self.buttons[idx].get_label())

    def set_tooltip(self, idx, strx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_tooltip_text(strx)

    def set_entry(self, idx, strx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_label(strx)

    def set_sensitive(self, idx, valx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_sensitive(valx)

    def get_size(self):
        return len (self.buttons)

    def set_check(self, idx, valx):
        if idx >= len(self.buttons):
            raise ValueError(IDXERR)
        self.buttons[idx].set_active(valx)
        self.buttons[idx].toggled()

    def get_check(self):
        cnt = 0
        for aa in (self.buttons):
            if aa.get_active():
                return cnt
            cnt += 1
        # Nothing selected ...
        return -1

    def get_text(self):
        for aa in (self.buttons):
            if aa.get_active():
                return aa.get_label()
        # Nothing selected ... empty str
        return ""

class Led(Gtk.DrawingArea):

    def __init__(self, color, size = 20, border = 2):
        GObject.GObject.__init__(self)
        #self.size_allocate();
        #self.size_request()
        self.border = border
        self.set_size_request(size + border, size + border)
        self.connect("draw", self.draw)
        self.color =  color

    def set_color(self, col):
        self.color = col
        self.queue_draw()

    def draw(self, area, cr):
        rect = self.get_allocation()
        #print ("draw", rect)

        #cr.rectangle(0, 0, rect.width, rect.height);
        #x = 0; y = 0; width = 10; height = 10
        #cr.save()
        #cr.translate(x + width / 2., y + height / 2.)
        #cr.scale(width / 2., height / 2.)
        #cr.restore()

        ccc = str2float(self.color)
        cr.set_source_rgba(ccc[0] * 0.7, ccc[1] * 0.7, ccc[2] * 0.7)
        cr.arc(rect.width/2, rect.height/2., rect.width/2., 0., 2 * math.pi)
        cr.fill()

        cr.set_source_rgba(ccc[0], ccc[1], ccc[2])
        cr.arc(rect.width/2, rect.height/2, rect.width / 2. * .8, 0., 2 * math.pi)
        cr.fill()

        # Reflection on the r
        cr.set_source_rgba(ccc[0], ccc[1] + 0.51, ccc[2])
        cr.arc(rect.width/2+1, rect.height/2, rect.width / 2. * .2, 0., 2 * math.pi)
        cr.fill()

# ------------------------------------------------------------------------

class Lights(Gtk.Frame):

    def __init__(self, col_arr, size = 6, call_me = None):

        GObject.GObject.__init__(self)
        self.box_arr = []
        vboxs = Gtk.VBox()
        vboxs.set_spacing(4);
        vboxs.set_border_width(4)

        for aa in col_arr:
            box = self.colbox(str2float(aa), size)
            vboxs.pack_start(box, False, False, False)
            self.box_arr.append(box)

        self.add(vboxs)

    def set_color(self, idx, col):
        if idx >= len(self.box_arr):
            raise ValueError(IDXERR)
        self.box_arr[idx].modify_bg(Gtk.StateFlags.NORMAL, str2col(col))

    def set_colors(self, colarr):
        for idx in range(len(self.box_arr)):
            self.box_arr[idx].modify_bg(
                        Gtk.StateFlags.NORMAL, str2col(colarr[idx]))

    def set_tooltip(self, idx, strx):
        if idx >= len(self.box_arr):
            raise ValueError(IDXERR)
        self.box_arr[idx].set_tooltip_text(strx)

    def set_tooltips(self, strarr):
        for idx in range(len(self.box_arr)):
            self.box_arr[idx].set_tooltip_text(strarr[idx])

    def get_size(self):
        return len (self.box_arr)

    def colbox(self, col, size):

        lab1 = Gtk.Label("  " * size + "\n" * (size // 3))
        lab1.set_lines(size)
        eventbox = Gtk.EventBox()
        frame = Gtk.Frame()
        frame.add(lab1)
        eventbox.add(frame)
        eventbox.color =  col  # Gtk.gdk.Color(col)
        eventbox.modify_bg(Gtk.StateFlags.NORMAL, float2col(eventbox.color))
        return eventbox

class WideButt(Gtk.Button):

    def __init__(self, labelx, callme = None, space = 2):
        #super().__init__(self)
        GObject.GObject.__init__(self)
        self.set_label(" " * space + labelx + " " * space)
        self.set_use_underline (True)
        if callme:
            self.connect("clicked", callme)

class FrameTextView(Gtk.TextView):

    def __init__(self, callme = None):

        GObject.GObject.__init__(self)
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_size_request(100, 100)
        self.scroll.add_with_viewport(self)
        self.frame = Gtk.Frame()
        self.frame.add(self.scroll)

        self.set_buffer(Gtk.TextBuffer())
        self.set_size_request(150, 150)
        ls = self.get_style_context()
        fd = ls.get_font(Gtk.StateFlags.NORMAL)
        #newfd = fd.to_string() + " " + str(fd.get_size() / Pango.SCALE + 4)
        #print("newfd", newfd)
        self.modify_font(Pango.FontDescription("Sans 13"))

    def append(self, strx):
        buff = self.get_buffer()
        old = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)
        buff.set_text(old + "\n" +  strx)
        usleep(20)
        #mainwin.statb2.scroll_to_iter(buff.get_end_iter(), 1.0, True, 0.1, 0.1)
        sb = self.scroll.get_vscrollbar()
        sb.set_value(2000000)

class Label(Gtk.Label):
    def __init__(self, textm = "", widget = None, tooltip=None, font = None):
        GObject.GObject.__init__(self)
        self.set_text_with_mnemonic(textm)
        if widget:
            self.set_mnemonic_widget(widget)
        if tooltip:
            self.set_tooltip_text(tooltip)
        if font:
            self.modify_font(Pango.FontDescription(font))


class Logo(Gtk.VBox):

    def __init__(self, labelx, tooltip = None, callme = None):

        GObject.GObject.__init__(self)

        self.logolab = Gtk.Label(labelx)
        self.logolab.set_has_window(True)
        if tooltip:
            self.logolab.set_tooltip_text(tooltip)

        self.logolab.set_events( Gdk.EventMask.BUTTON_PRESS_MASK |
                             Gdk.EventMask.BUTTON_RELEASE_MASK )

        if callme:
            self.logolab.connect("button-press-event", callme)

        self.logolab.modify_font(Pango.FontDescription('Times 45'))

        #self.pack_start(Spacer(), 0, 0, False)
        self.pack_start(self.logolab, 0, 0, False)
        #self.pack_start(Spacer(), 0, 0, False)

    def forallcallb(self, arg1):
        #print ("arg1", arg1)
        arg1.hide();

    def hide(self):
        self.forall(self.forallcallb)

# ------------------------------------------------------------------------
# An N pixel horizontal spacer. Defaults to X pix

class xSpacer(Gtk.HBox):

    def __init__(self, sp = None):
        GObject.GObject.__init__(self)
        #self.pack_start()
        if gui_testmode:
            col = randcolstr(100, 200)
            self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(col))
        if sp == None:
            sp = 6
        self.set_size_request(sp, sp)


class ScrollListBox(Gtk.Frame):

    def __init__(self, limit = -1, colname = '', callme = None):
        Gtk.Frame.__init__(self)
        self.listbox = ListBox(limit, colname)
        if callme:
            self.listbox.set_callback(callme)
        self.listbox.scroll = Gtk.ScrolledWindow()
        self.listbox.scroll.add_with_viewport(self.listbox)
        self.add(self.listbox.scroll)
        self.autoscroll = True

    # Propagate needed ops to list control

    def append_end(self, strx):
        #print("ser str append", strx)
        self.listbox.append(strx)

        if self.autoscroll:
            usleep(10)              # Wait for it to go to screen
            sb = self.listbox.scroll.get_vscrollbar()
            sb.set_value(2000000)
        self.listbox.select(-1)

    def clear(self):
        self.listbox.clear()

    def select(self, num):
        self.listbox.select(num)

# ------------------------------------------------------------------------
# This override covers / hides the complexity of the treeview and the
# textlisbox did not have the needed detail

class ListBox(Gtk.TreeView):

    def __init__(self, limit = -1, colname = ''):

        self.limit = limit
        self.treestore = Gtk.TreeStore(str)
        Gtk.TreeView.__init__(self, self.treestore)

        cell = Gtk.CellRendererText()
        # create the TreeViewColumn to display the data
        tvcolumn = Gtk.TreeViewColumn(colname)
        # add the cell to the tvcolumn and allow it to expand
        tvcolumn.pack_start(cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        tvcolumn.add_attribute(cell, 'text', 0)

        # add tvcolumn to treeview
        self.append_column(tvcolumn)
        self.set_activate_on_single_click (True)

        self.callb = None
        self.connect("row-activated",  self.tree_sel)

    def tree_sel(self, xtree, xiter, xpath):
        #print("tree_sel", xtree, xiter, xpath)
        sel = xtree.get_selection()
        xmodel, xiter = sel.get_selected()
        if xiter:
            xstr = xmodel.get_value(xiter, 0)
            #print("Selected", xstr)
            if self.callb:
                self.callb(xstr)
        pass

    def set_callback(self, funcx):
        self.callb = funcx

    # Delete previous contents
    def clear(self):
        try:
            while True:
                root = self.treestore.get_iter_first()
                if not root:
                    break
                try:
                    self.treestore.remove(root)
                except:
                    print("except: treestore remove")

        except:
            print("update_tree", sys.exc_info())
            pass

    # Select Item. -1 for select none; Rase Valuerror for wrong index.
    def select(self, idx):
        ts = self.get_selection()
        if idx == -1:
            ts.unselect_all()
            return
        iter = self.treestore.get_iter_first()
        for aa in range(idx):
            iter = self.treestore.iter_next(iter)
            if not iter:
                break
        if not iter:
            pass
            #raise ValueError("Invalid selection index.")
        ts.select_iter(iter)

    # Return the number of list items
    def get_size(self):
        cnt = 0
        iter = self.treestore.get_iter_first()
        if not iter:
            return cnt
        cnt = 1
        while True:
            iter = self.treestore.iter_next(iter)
            if not iter:
                break
            cnt += 1
        return cnt

    def get_item(self, idx):
        cnt = 0; res = ""
        iter = self.treestore.get_iter_first()
        if not iter:
            return ""
        cnt = 1
        while True:
            iter = self.treestore.iter_next(iter)
            if not iter:
                break
            if cnt == idx:
                res = self.treestore.get_value(iter, 0)
                break
            cnt += 1
        return res

    def append(self, strx):
        if self.limit != -1:
            # count them
            cnt = self.get_size()
            #print("limiting cnt=", cnt, "limit=", self.limit)
            for aa in range(cnt - self.limit):
                iter = self.treestore.get_iter_first()
                if not iter:
                    break
                try:
                    self.treestore.remove(iter)
                except:
                    print("except: treestore remove lim")

        last = self.treestore.append(None, [strx])
        self.set_cursor_on_cell(self.treestore.get_path(last), None, None, False)

    def get_text(self):
        sel = self.get_selection()
        xmodel, xiter = sel.get_selected()
        if xiter:
            return xmodel.get_value(xiter, 0)

    # Get current IDX -1 for none
    def get_curridx(self):
        sel = self.get_selection()
        xmodel, xiter = sel.get_selected()
        if not xiter:
            return -1

        # Count back from match
        cnt = 0
        while True:
            xiter = self.treestore.iter_previous(xiter)
            if not xiter:
                break
            #print ("xiter:", xiter)
            cnt += 1
        return cnt

# ------------------------------------------------------------------------
# Highlite test items

def set_testmode(flag):
    global gui_testmode
    gui_testmode = flag

if __name__ == '__main__':
    print("This file was not meant to run as the main module")

# ------------------------------------------------------------------------
# Highlite test items

def set_gui_testmode(flag):
    global gui_testmode
    gui_testmode = flag

if __name__ == '__main__':
    print("This file was not meant to run as the main module")

# EOF




