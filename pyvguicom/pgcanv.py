#!/usr/bin/env python3

#pylint: disable=C0103
#pylint: disable=C0209
#pylint: disable=C0321
#pylint: disable=C0116
#pylint: disable=W0301
#pylint: disable=C0410
#pylint: disable=C0413

import os, time, sys, datetime, warnings, math, pickle
import binascii

import gi; gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango
from gi.repository import cairo

gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

import pggui
import pgdlgs
import pgutils
import pgtests
import pgbutt
import canvdlg
import canvobjs

''' Python Canvas '''

piclename = "outline.pickle"
untitled = "untitled.ped"
signon = "PGCANV Version 1.0.0\n"

canv_testmode = 0

def set_canv_testmode(flag):
    global canv_testmode
    canv_testmode = flag


class Canvas(Gtk.DrawingArea):

    def __init__(self, parent, statbox = None, config = None):

        self.config = config
        self.parent = parent
        self.statcall = None

        if self.config.verbose > 2:
            print(config)
        Gtk.DrawingArea.__init__(self)
        self.changed = False
        self.statbox = statbox
        self.parewin = parent
        self.set_can_focus(True)
        self.set_events(Gdk.EventMask.ALL_EVENTS_MASK)

        self.connect("draw", self.draw_event)
        self.connect("motion-notify-event", self.area_motion)
        self.connect("button-press-event", self.area_button)
        self.connect("button-release-event", self.area_button)
        self.connect("key-press-event", self.area_key)
        #self.connect("focus-in-event", self.focus_in)

        self.coll = []
        self.cnt = 0
        self.drag = None
        self.curl = None
        self.resize = None
        self.dragcoord = (0,0)
        self.size2 = (0,0)
        self.noop_down = False
        self.drawline = False
        self.stroke = []
        warnings.simplefilter("ignore")
        self.hand = Gdk.Cursor(Gdk.CursorType.HAND1)
        self.arrow = Gdk.Cursor(Gdk.CursorType.ARROW)
        self.sizing =  Gdk.Cursor(Gdk.CursorType.SIZING)
        self.cross =  Gdk.Cursor(Gdk.CursorType.TCROSS)
        self.hair =  Gdk.Cursor(Gdk.CursorType.CROSSHAIR)
        self.curve =  Gdk.Cursor(Gdk.CursorType.TARGET)
        self.pencil =  Gdk.Cursor(Gdk.CursorType.PENCIL)
        warnings.simplefilter("default")
        self.fname = untitled
        self.popbase = pgbutt.PopBase(self.parent)
        dd = Gdk.Display.get_default()
        self.clip = Gtk.Clipboard.get_default(dd)

    def _selone(self, curr):
        for bb in self.coll:
            if bb.selected:
                bb.selected = False
        curr.selected = True

    def area_key(self, area, event):
        if self.config.debug > 6:
            print ("area_key", event.keyval)
        if event.keyval == Gdk.KEY_Delete or event.keyval == Gdk.KEY_KP_Delete:
            #print("Del key")
            for bb in self.coll:
                if bb.selected:
                    #print("would delete", bb)
                    self.coll.remove(bb)
                    self.show_status("Deleted Item '%s'" % bb.text)
            self.queue_draw()

        if event.keyval == Gdk.KEY_Up:
            #if self.config.debug > 6:
            #    print("UP key")
            pass

        if event.keyval == Gdk.KEY_Down:
            #if self.config.debug > 6:
            #        print("DN key")
            pass

        return True

    def show_status(self, strx):
        if self.statcall:
            self.statcall.set_status_text(strx)
        self.popbase.submit(strx, 1000 + len(strx) * 400)

    def area_motion(self, area, event):
        #print ("motion event", event.state, event.x, event.y)
        if self.drag:
            self.changed = True
            gdk_window = self.get_root_window()
            gdk_window.set_cursor(self.hand)
            #print ("drag coord", self.dragcoord[0],  self.dragcoord[1], event.x, event.y)
            xd = int(self.dragcoord[0] - event.x)
            yd = int(self.dragcoord[1] - event.y)
            #print ("delta", xd, yd)
            for aa in self.coll:
                if aa.selected:
                    aa.rect.x = aa.orgdrag.x  - xd
                    aa.rect.y = aa.orgdrag.y  - yd
                    # Also move whole group IN NOT SHIFT
                    if aa.groupid and not event.state & Gdk.ModifierType.SHIFT_MASK :
                        for bb in self.coll:
                            if aa.groupid == bb.groupid:
                                bb.rect.x = bb.orgdrag.x  - xd
                                bb.rect.y = bb.orgdrag.y  - yd
            self.queue_draw()

        elif self.curl:
            gdk_window = self.get_root_window()
            gdk_window.set_cursor(self.pencil)
            xd = int(self.dragcoord[0] - event.x)
            yd = int(self.dragcoord[1] - event.y)
            #print ("curl rdelta", xd, yd)
            self.changed = True
            self.queue_draw()

        elif self.resize:
            gdk_window = self.get_root_window()
            gdk_window.set_cursor(self.sizing)
            #print ("resize", self.resize.text,  event.x, event.y)
            xd = int(self.dragcoord[0] - event.x)
            yd = int(self.dragcoord[1] - event.y)
            #print ("rdelta", xd, yd)

            #if self.size2[0] - xd > 2:
            self.resize.rect.w = self.size2[0] - xd
            #if self.size2[1] - yd > 2:
            self.resize.rect.h = self.size2[1] - yd

            #print("resize rect", self.resize.rect.w, self.resize.rect.h)
            #if self.resize.rect.h < 0:
            #    self.resize.rect.y -= 2 * abs(self.resize.rect.h)
            #    self.resize.rect.h = abs(self.resize.rect.h)
            self.changed = True
            self.queue_draw()
        else:
            onmarker = 0 #False
            hit = pggui.Rectangle(event.x, event.y, 2, 2)
            # Check if on marker
            for cc in self.coll:
                mark = cc.hitmarker(hit)
                if mark:
                    onmarker = mark
                    break

            warnings.simplefilter("ignore")
            gdk_window = self.get_root_window()
            warnings.simplefilter("default")

            if onmarker == 5:
                gdk_window.set_cursor(self.pencil)
            elif onmarker:
                gdk_window.set_cursor(self.cross)
            elif self.noop_down:
                gdk_window.set_cursor(self.hair)
            else:
                gdk_window.set_cursor(self.arrow)

            '''if event.state & Gdk.ModifierType.SHIFT_MASK:
                print( "Shift ButPress x =", event.x, "y =", event.y)
            if event.state & Gdk.ModifierType.CONTROL_MASK:
                print( "Ctrl ButPress x =", event.x, "y =", event.y)
            if event.state & Gdk.ModifierType.MOD1_MASK :
                print( "Alt ButPress x =", event.x, "y =", event.y)
            else:'''

            if event.state & Gdk.ModifierType.BUTTON1_MASK:
                #print( "But Drag", event.state, "x =", int(event.x), "y =", int(event.y))
                self.stroke.append((int(event.x), int(event.y)))
                self.queue_draw()

    def findsel(self):
        cc = None
        for bb in self.coll:
            if bb.selected:
                cc = bb
                break
        return cc

    def area_button(self, area, event):

        self.grab_focus()
        self.mouse = pggui.Rectangle(event.x, event.y, 4, 4)

        if self.config.debug > 3:
            if event.state & Gdk.ModifierType.SHIFT_MASK:
                print( "Shift ButPress x =", event.x, "y =", event.y)
            elif event.state & Gdk.ModifierType.CONTROL_MASK:
                print( "Ctrl ButPress x =", event.x, "y =", event.y)
            else:
                print( "Button:", event.button, "state:", event.state,
                                     " x =", event.x, "y =", event.y)
        if  event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            cc = self.findsel()
            if not cc:
                return
            if self.config.debug > 3:
                print("DBL click", event.button, cc)
            response, txt = canvdlg.textdlg(cc.text, self.get_toplevel())
            if response == Gtk.ResponseType.ACCEPT:
                #print("Got text", txt)
                cc.text = txt
                self.changed = True
                self.queue_draw()
            self.drag = None
            return

        if  event.type == Gdk.EventType.BUTTON_RELEASE:
            self.curl = None
            self.drag = None
            self.resize = None
            self.noop_down = False
            if self.drawline:
                self.drawline = False
                #print("stroke", self.stroke)
                if len(self.stroke) > 4:
                    self.show_status( \
                        "Added freehand line: %d segments" % len(self.stroke))
                    rstr = "" #randstr(6)
                    coord = pggui.Rectangle(canvobjs.stroke_dims(self.stroke))
                    self.add_stroke(coord, rstr, pggui.randcolstr(),
                                        arr = self.stroke)
                self.stroke = []
            self.get_root_window().set_cursor(self.arrow)

        if  event.type == Gdk.EventType.BUTTON_PRESS:
            hit = pggui.Rectangle(event.x, event.y, 2, 2)
            hitx = None
            if event.button == 1:
                #if not event.state & Gdk.ModifierType.SHIFT_MASK and \
                #            not event.state & Gdk.ModifierType.CONTROL_MASK:
                if not event.state & Gdk.ModifierType.CONTROL_MASK:
                    # Operate on pre selected
                    if self.drag:
                        return
                    for bb in self.coll:
                        if not bb.selected:
                            continue
                        hitx = bb.hittest(hit)
                        hity = bb.hitmarker(hit)
                        #print("Operate on selected", bb.id)
                        if hity == 5:
                            #print("Hit on curve marker")
                            self.resize = None
                            self.drag = None
                            self.curl = bb
                            self.dragcoord  = (event.x, event.y)
                        elif hity:
                            #print("Hit on marker")
                            self.resize = bb
                            self.drag = None
                            self.dragcoord  = (event.x, event.y)
                            self.size2 = (self.resize.rect.w, self.resize.rect.h)
                            return
                        elif hitx:
                            self.drag = bb
                            self.dragcoord  = (event.x, event.y)
                            for cc in self.coll:
                                if cc.selected:
                                    cc.orgdrag = cc.rect.copy()
                                    # Also move whole group
                                    if cc.groupid:
                                        for bb in self.coll:
                                            if cc.groupid == bb.groupid:
                                                bb.orgdrag = bb.rect.copy()
                        else:
                            pass

                direction = not event.state & Gdk.ModifierType.SHIFT_MASK
                #print("direction", direction)
                sortx = sorted(self.coll, reverse = direction,
                            key = lambda item: item.zorder)

                # Execute new hit test on drag immidiate
                for aa in sortx:
                    if aa.hittest(hit): # and aa.selected:
                        hitx = aa
                        self.drag = aa
                        self.dragcoord  = (event.x, event.y)
                        aa.orgdrag = aa.rect.copy()
                        # Also move whole group
                        if aa.groupid:
                            for bb in self.coll:
                                if bb.groupid == aa.groupid:
                                    bb.orgdrag = bb.rect.copy()
                        break

                #for bb in self.coll:
                for bb in sortx:
                    if bb == hitx:
                        if event.state & Gdk.ModifierType.CONTROL_MASK:
                            bb.selected = not bb.selected
                        else:
                            bb.selected = True
                            #break
                    else:
                        if event.state & Gdk.ModifierType.SHIFT_MASK or \
                            event.state & Gdk.ModifierType.CONTROL_MASK:
                            pass
                        else:
                            bb.selected = False

                if not hitx:
                    self.noop_down = True
                    warnings.simplefilter("ignore")
                    gdk_window = self.get_root_window()
                    warnings.simplefilter("default")
                    gdk_window.set_cursor(self.hair)

                    # Turn on draw
                    self.drawline = True

                self.queue_draw()

            elif event.button == 3:
                #print("Right click")
                bb = None
                # Execute new hit test
                for aa in self.coll:
                    if aa.hittest(hit):
                        bb = aa
                        break
                if bb:
                    cnt = 0
                    for aa in self.coll:
                        if aa.selected:
                            cnt += 1
                    if cnt == 0:
                        bb.selected = True

                    mms = ("Alignment",
                            "Align Left","Align Right",
                            "Align Top","Align Buttom",
                            "Align Mid X","Align Mid Y",)
                    warnings.simplefilter("ignore")
                    align = pggui.Menu(mms, self.menu_align, event, True)
                    warnings.simplefilter("default")

                    mmz = ( "Z-Order",
                            "To Front","To Back",
                            "One forward","One Backward",)
                    warnings.simplefilter("ignore")
                    zord = pggui.Menu(mmz, self.menu_zord, event, True)
                    warnings.simplefilter("default")

                    ccs = ( "Connect",
                            "Connect Objects", "Connect Objects (arrow ->)",
                            "Connect Objects (arrow <-)", "Disconnect Objects",)

                    cmenu = pggui.Menu(ccs, self.menu_connect, event, True)

                    if cnt > 1:
                        mmm = ("Multiple Selection", "Properties", cmenu,
                         "Group Objects", "Ungroup Objects", align, zord)
                        warnings.simplefilter("ignore")
                        pggui.Menu(mmm, self.menu_action, event)
                        warnings.simplefilter("default")
                    else:
                        mmm = (bb.text, "Object Properties", "Text",
                                "FG Color", "BG Color", "Ungroup",
                                        "Delete", zord,
                                        "-", "Copy", "Paste", )
                        warnings.simplefilter("ignore")
                        pggui.Menu(mmm, self.menu_action2, event)
                        warnings.simplefilter("default")
                    self.queue_draw()
                else:
                    mmm = ("Main Menu", "Add Rectangle", "Add Text",
                        "Add Rounded Rect", "Add Rombus", "Add Circle",
                        "Add Line", "Add Image",
                        "-", "Clear Canvas",
                        "-", "Copy", "Paste",
                        "-", "Open", "Open (append)", "Save", "Save As")
                    warnings.simplefilter("ignore")
                    pggui.Menu(mmm, self.menu_action3, event)
                    warnings.simplefilter("default")
            else:
                print("??? click", event.button)

    def writeout(self, fnamex):

        if not self.changed:
            self.show_status("Not changed: %s" % os.path.basename(fnamex))
            return

        if self.config.verbose:
            print("Saving to:", fnamex)
        sum = []
        ff = open(fnamex, "wb")
        sum = []
        pickle.dump(signon, ff)
        pickle.dump(len(self.coll), ff)
        for aa in self.coll:
            aa.selected = False
            try:
                pickle.dump(aa, ff)
            except:
                print(aa, sys.exc_info())
                pgutils.put_exception("Cannot pickle " + str(type(aa)))

        ff.close()
        self.show_status("Written: %s" % os.path.basename(fnamex))
        self.changed = False

    def menu_connect(self, item, num):
        #print ("Connect", item, num)
        if num >= 1 and num <= 3:
            print ("Conn obj", item, num)
            ccc = []
            for aa in self.coll:
                if aa.selected:
                    ccc.append(aa)
            for aa in ccc[1:]:
                self.show_status("Connecting: %s" % aa.text)
                ccc[0].others.append((aa.id, num))
                self.changed = True
        if num == 4:
            ccc = []
            for aa in self.coll:
                if aa.selected:
                    ccc.append(aa)

            if len(ccc) == 2:
                self.show_status("Disconnecting: %s from %s" % \
                                           (ccc[0].text, ccc[1].text))
                try:
                    ccc[0].others = []
                    self.changed = True
                except: pass
            else:
                for dd in ccc:
                    dd.others = []
                    self.changed = True
            self.queue_draw()

    def menu_zord(self, item, num):

        #print ("Z order", item, num)
        if num == 1:
            for aa in self.coll:
                if aa.selected:
                    canvobjs.DrawObj.globzorder = canvobjs.DrawObj.globzorder + 1
                    aa.zorder = canvobjs.DrawObj.globzorder
                    self.changed = True
                    break

        if num == 2:
            for aa in self.coll:
                aa.zorder += 1
            for aa in self.coll:
                if aa.selected:
                    aa.zorder = 0
                    self.changed = True
                    break

        self.queue_draw()

    def menu_align(self, item, num):

        #print ("Align", item, num)

        mark = -1
        if "Left" in item:
            for aa in self.coll:
                if aa.selected:
                    if mark == -1:
                        mark = aa.rect.x
                        continue
                    aa.rect.x = mark
                    self.changed = True

        if "Top" in item:
            for aa in self.coll:
                if aa.selected:
                    if mark == -1:
                        mark = aa.rect.y
                        continue
                    aa.rect.y = mark
                    self.changed = True

        if "Right" in item:
            for aa in self.coll:
                if aa.selected:
                    if mark == -1:
                        mark = aa.rect.x + aa.rect.w
                        continue
                    aa.rect.x = mark - aa.rect.w
                    self.changed = True

        if "Mid X" in item:
            for aa in self.coll:
                if aa.selected:
                    if mark == -1:
                        mark = aa.center()[0]
                        continue
                    aa.rect.x = mark - aa.rect.w / 2
                    self.changed = True

        if "Mid Y" in item:
            for aa in self.coll:
                if aa.selected:
                    if mark == -1:
                        mark = aa.center()[1]
                        continue
                    aa.rect.y = mark - aa.rect.h / 2
                    self.changed = True

    def menu_action(self, item, num):

        #print("menu_action:", item, num)

        # Prop
        if num == 1:
            props = []
            for aa in self.coll:
                if aa.selected:
                    props.append(aa)
            if props:
                canvdlg.propdlg(props, self.get_toplevel())
            else:
                self.show_status("Property dialog: Nothing selected")
        # Group
        if num == 3:
            canvobjs.DrawObj.globgroup += 1
            print("Group", canvobjs.DrawObj.globgroup)
            for aa in self.coll:
                if aa.selected:
                    aa.groupid = canvobjs.DrawObj.globgroup
        # Ungroup
        if num == 4:
            print("unGroup", canvobjs.DrawObj.globgroup)
            for aa in self.coll:
                if aa.selected:
                    for bb in self.coll:
                        if aa.groupid == bb.groupid:
                            bb.groupid = 0
                        aa.groupid = 0
        # Align
        if num == 5:
            for aa in self.coll:
                if aa.selected:
                    for bb in self.coll:
                        if bb.selected:
                            bb.rect.x = aa.rect.x
                    break
        self.queue_draw()

    def menu_action2(self, item, num):

        if self.config.verbose:
            print("menu_action2", item, num)

        if num == 1:
            #print("Getting properties")
            props = []
            for aa in self.coll:
                if aa.selected:
                    props.append(aa)
            if props:
                canvdlg.propdlg(props, self.get_toplevel())
                self.queue_draw()
            else:
                self.show_status("Property dialog: Nothing selected")

        if num == 2:
            #print("Getting text")
            bb = None
            for aa in self.coll:
                if aa.selected:
                    bb = aa
            if bb:
                #print("Getting text", bb)
                response, txt = canvdlg.textdlg(bb.text, self.get_toplevel())
                if response == Gtk.ResponseType.ACCEPT:
                    #print("Got text", txt)
                    bb.text = txt
                    self.queue_draw()

        if num == 3:
            colx = None
            for aa in self.coll:
                if aa.selected:
                    colx = aa
            ccc = canvdlg.canv_colsel(colx.col2, "Foreground Color")
            for aa in self.coll:
                if aa.selected:
                    aa.col2 = ccc
            self.queue_draw()

        if num == 4:
            colx = None
            for aa in self.coll:
                if aa.selected:
                    colx = aa
            ccc = canvdlg.canv_colsel(colx.col1, "Background Color")
            for aa in self.coll:
                if aa.selected:
                    aa.col1 = ccc
            self.queue_draw()

        if num == 5:
            for aa in self.coll:
                if aa.selected:
                    for bb in self.coll:
                        if aa.groupid == bb.groupid:
                            bb.groupid = 0
                        aa.groupid = 0
            self.queue_draw()

        if num == 6:
            #print("Delete")
            for bb in self.coll:
                if bb.selected:
                    #print("would delete", bb)
                    self.coll.remove(bb)
                    self.show_status("Deleted Item: '%s'" % bb.text)
            self.queue_draw()

        if num == 9:
            self.copy()

        if num == 10:
            self.paste()

    def menu_action3(self, item, num):

        if self.config.verbose > 2:
            print("menu action3 ", item, num)

        if "Dump" in item:
            for aa in self.coll:
                print(aa.dump())

        elif "Rectangle" in item:
            rstr = pgtests.randstr(6)
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 120, 120)
            self.add_rect(coord, rstr, "#0000000") # pggui.randcolstr())

        elif "Image" in item:
            rstr = pgtests.randstr(6)
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 120, 120)
            self.add_image(coord, rstr, "#0000000") # pggui.randcolstr())

        elif "Romb" in item:
            rstr = pgtests.randstr(6)
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 120, 120)
            self.add_romb(coord, rstr, pggui.randcolstr())

        elif "Rounded" in item:
            rstr = pgtests.randstr(6)
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 120, 120)
            self.add_rrect(coord, rstr, pggui.randcolstr())

        elif "Circ" in item:
            rstr = pgtests.randstr(6)
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 70, 70)
            self.add_circle(coord, rstr, pggui.randcolstr())

        elif "Text" in item:
            rstr = "Edit text here ... "
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 16, 16)
            self.add_text(coord, rstr, "#000000") # pggui.randcolstr())

        elif "Line" in item:
            rstr = pgtests.randstr(6)
            coord = pggui.Rectangle(self.mouse.x, self.mouse.y, 40, 40)
            self.add_line(coord, rstr, pggui.randcolstr())

        elif "Load" in item:
            self.readfile(piclename)

        elif "Persist" in item:
            self.writeout(piclename)

        elif "Copy" in item:
            #print("Copy")
            self.copy()

        elif "Paste" in item:
            #print("Paste")
            self.paste()

        elif "Clear" in item:
            # Clear canvas
            self.coll = []
            self.queue_draw()

        elif "Export" in item:
            #print("Export")
            # Create PNG
            for aa in self.coll:
                aa.selected = False
            self.queue_draw()
            pggui.usleep(10)
            rect = self.get_allocation()

            #pixbuf = Gdk.pixbuf_get_from_window(self.get_window(), 0, 0, rect.width, rect.height)
            #self.surface = cairo.create_for_rectangle(0, 0, width, height)
            #self.surface = cairo.create_similar_image(cairo.Format.ARGB32, rect.width, rect.height)
            #cr =  self.get_window().cairo_create()
            #cr =  cairo.Context(self.surface)

            cr = Gdk.cairo_create(self.get_window())
            self.draw_event(self, cr)
            pixbuf = Gdk.pixbuf_get_from_surface(cr.get_target(), 0, 0, rect.width, rect.height)
            pixbuf.savev("buff.png", "png", [None], [])

        elif "append" in item:
            if self.config.verbose:
                print("Open append")
            self.open(True)

        elif "Open" in item:
            if self.config.verbose:
                print("Open")
            self.open()

        elif "Save As" in item:
            if self.config.verbose:
                print("Save As")
                #fff = pgdlgs.savedialog(self.fname)
            self.saveas()

        elif "Save" in item:
            if self.config.verbose:
                print("Save")
            self.save()

        else:
            print("Invalid menu item")

    def copy(self):
        carr = []
        for aa in self.coll:
            if aa.selected:
                carr.append(aa)
                clipobj = pickle.dumps(aa)
                hex_data = binascii.hexlify(clipobj).decode()
                self.clip.set_text(hex_data, -1)
        if not carr:
            return

    def paste(self):
        hex_data = self.clip.wait_for_text()
        clipobj = binascii.unhexlify(hex_data.encode())
        aa = pickle.loads(clipobj)
        aa.rect.x = self.mouse.x ; self.rect.y = self.mouse.y
        aa.id = pgtests.randlett(8)
        self.coll.append(aa)
        self.queue_draw()

    def save(self):
        if self.config.verbose:
            print("Save")
        if not self.coll:
            pgdlgs.message("Empty document.")
            return
        if self.fname == untitled:
            fnamex = pgdlgs.savedialog(self.fname)
            if not fnamex:
                return
            self.fname = fnamex
        self.writeout(self.fname)

    def saveas(self):
        if self.config.verbose:
            print("Saveas")
        if not self.coll:
            pgdlgs.message("Empty document.")
            return
        fnamex = pgdlgs.savedialog(self.fname)
        if not fnamex:
            return
        self.fname = fnamex
        self.changed = True
        self.writeout(self.fname)

    def open(self, keep = False):
        if self.config.verbose:
            print("Open")
        filter =  [ ("*.ped", "PED files (*.ped)"),
                    ("*.*", "ALL files (*.*)"),
                  ]
        fff = pgdlgs.opendialog(filter=filter)
        if not fff:
            return

        if self.config.verbose:
            print("Open filename:", fff)

        # Clear canvas if requested
        if not keep:
            self.coll = []

        self.queue_draw()
        self.readfile(fff)
        self.fname = fff
        self.queue_draw()

    def show_objects(self):
        for aa in self.coll:
            print ("GUI Object", aa)

    def readfile(self, fnamex):
        ff = open(fnamex, "rb")
        sig = pickle.load(ff)
        try:
            if "PGCANV" not in sig:
                raise ValueError
        except:
            self.show_status("Not a valid pgcanv file: '%s'" % os.path.basename(fnamex))
            ff.close()
            return

        if "1.0.0" not in sig:
            print("warning: not a version 1.0.0 file")

        aa = pickle.load(ff)
        for aa in range(aa):
            try:
                aa = pickle.load(ff)
            except EOFError:
                break
            except:
                pgutils.put_exception("Cannot load " + str(type(aa)))
                break
            self.coll.append(aa)
        ff.close()

        if self.config.debug > 0:
            self.show_objects()

        self.show_status("Loaded: '%s'" % os.path.basename(fnamex))
        self.queue_draw()

    # Add rectangle to collection of objects
    def add_rect(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.RectObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.queue_draw()
        self.show_status("Added rectangle '%s'" % rob.text)
        self.changed = True
        return rob

    # Add rectangle to collection of objects
    def add_image(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.ImgObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.queue_draw()
        self.show_status("Added image '%s'" % rob.text)
        self.changed = True
        return rob

    def add_line(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.LineObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.queue_draw()
        self.show_status("Added line '%s'" % rob.text)
        self.changed = True
        return rob

    def add_curve(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.CurveObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.queue_draw()
        self.show_status("Added curve '%s'" % rob.text)
        self.changed = True
        return rob

    def add_text(self, coord, text, crf, crb="#ffffff", border=2, fill=False):
        col1 = pggui.str2float(crb);  col2 = pggui.str2float(crf)
        rob = canvobjs.TextObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.queue_draw()
        self.show_status("Added text '%s'" % rob.text)
        self.changed = True
        return rob

    def add_circle(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.CircObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.show_status("Added circle '%s'" % rob.text)
        self.queue_draw()
        self.changed = True
        return rob

    def add_stroke(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False, arr = []):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.StrokeObj(coord, text, col1, col2, border, fill, arr)
        self.coll.append(rob)
        self._selone(rob)
        self.show_status("Added stroke '%s'" % rob.text)
        self.queue_draw()
        self.changed = True
        return rob

    def add_romb(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob = canvobjs.RombObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.show_status("Added rombus '%s'" % rob.text)
        self.queue_draw()
        self.changed = True
        return rob

    def add_rrect(self, coord, text, crf, crb = "#ffffff", border = 2, fill = False):
        col1 = pggui.str2float(crb);    col2 = pggui.str2float(crf)
        rob  = canvobjs.RoundRectObj(coord, text, col1, col2, border, fill)
        self.coll.append(rob)
        self._selone(rob)
        self.show_status("Added rounded rect '%s'" % rob.text)
        self.queue_draw()
        self.changed = True
        return rob

    def _calc_angle(self, aac, bbc):

        dd = bbc[1] - aac[1] ; ee = bbc[0] - aac[0]
        try:
            rat = abs(dd / ee)
        except:
            # Fake infinity
            rat  = 1000
        atan  = math.atan(rat)
        deg = math.degrees(atan)
        #print("dd:", dd, "ee:", ee, "deg: %0.2f" % deg)

        # Determine quadrant
        base = 0
        if ee < 0 and dd < 0:
            base = 180 + deg
        elif ee < 0:
            base = 90 + (90 - deg)
        elif dd < 0:
            base = 270 + (90 - deg)
        else:
            base = deg
        return base

    def draw_event(self, doc, cr):
        #print ("Painting .. ", self.cnt)
        self.cnt += 1
        ctx = self.get_style_context()
        fg_color = ctx.get_color(Gtk.StateFlags.NORMAL)
        #bg_color = ctx.get_background_color(Gtk.StateFlags.NORMAL)

        self.layout = PangoCairo.create_layout(cr)
        self.rect = self.get_allocation()
        self.cr = cr
        self.crh = pggui.CairoHelper(cr)

        # Paint white, ignore system BG
        border = 4
        cr.set_source_rgba(255/255, 255/255, 255/255)
        cr.rectangle( border, border, self.rect.width - border * 2, self.rect.height - border * 2)
        cr.fill()

        # Draw connections
        cr.set_source_rgba(55/255, 55/255, 55/255)
        for aa in self.coll:
            for cc, dd in aa.others:
                for bb in self.coll:
                    if cc == bb.id:
                        #print("connect draw", aa.text, bb.text, dd)
                        aac = aa.center()
                        cr.move_to(aac[0], aac[1])
                        bbc = bb.center()
                        cr.line_to(bbc[0], bbc[1])
                        cent = [(aac[0] + bbc[0]) / 2, (aac[1] + bbc[1]) / 2]
                        if dd == 1:
                            pass
                        elif dd == 2:
                            #print("Arrow left")
                            deg = self._calc_angle(aac, bbc)
                            #print("deg: %0.2f" % deg )
                            #cr.set_source_rgba(0/255, 0/255, 0/255)
                            # Offset by half arrow
                            #cent[0] += 12 * (math.sin(rads))
                            #cent[1] += 12 * (math.cos(rads))
                            cr.move_to(*cent)
                            rads = math.radians(deg - 70)
                            cr.line_to(cent[0] + 24 * (math.sin(rads)),
                                       cent[1] - 24 * (math.cos(rads)) )
                            cr.move_to(*cent)
                            rads = math.radians(deg - 110)
                            cr.line_to(cent[0] + 24 * (math.sin(rads)),
                                       cent[1] - 24 * (math.cos(rads)) )
                        elif dd == 3:
                            #print("Arrow right")
                            deg = self._calc_angle(aac, bbc)
                            #print("deg: %0.2f" % deg )
                            #cr.set_source_rgba(0/255, 0/255, 0/255)
                            rads = math.radians(deg - 70)
                            #cent[0] += 12 * (math.sin(rads))
                            #cent[1] += 12 * (math.cos(rads))
                            cr.move_to(*cent)
                            cr.line_to(cent[0] - 24 * (math.sin(rads)),
                                       cent[1] + 24 * (math.cos(rads)) )
                            cr.move_to(*cent)
                            rads = math.radians(deg - 110)
                            cr.line_to(cent[0] - 24 * (math.sin(rads)),
                                       cent[1] + 24 * (math.cos(rads)) )
                        cr.stroke()

        sortx = sorted(self.coll, reverse = False, key = lambda item: item.zorder)

        # Draw objects
        #for aa in self.coll:
        for aa in sortx:
            try:
                aa.draw(cr, self)
            except:
                pgutils.put_exception("Cannot draw " + str(type(aa)))
                #aa.dump()

        init = 0
        for aa, bb in self.stroke:
            if init == 0:
                self.cr.move_to(aa, bb)
            else:
                self.cr.line_to(aa, bb)
            init += 1
        self.cr.stroke()

    def dumpobjs(self):
        for aa in self.coll:
            aa.dump()


# EOF
