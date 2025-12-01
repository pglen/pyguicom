#!/usr/bin/env python3

#pylint: disable=C0103
#pylint: disable=C0209
#pylint: disable=C0321
#pylint: disable=C0116
#pylint: disable=W0301
#pylint: disable=C0410
#pylint: disable=C0413

import os
#, time, sys, datetime, warnings, math
#import signal, subprocess, platform, ctypes, sqlite3,

import gi; gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from gi.repository import GLib
from gi.repository import Pango
from gi.repository import GdkPixbuf
from gi.repository import cairo

gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

__doc__ = ''' Objects for canvas '''

import pggui
import pgtests

#RECT, TEXT, CIRC, ROMB, FREE = range(5)

class DrawObj(object):

    ''' Base class for all drawing objects '''

    globzorder = 0 ; globgroup = 0

    def __init__(self,  rect, text, col1, col2, border, fill):

        self.rect = rect
        self.text = text
        self.col1 = col1
        self.col2 = col2
        self.border = border
        self.fill = fill
        self.selected = False
        self.id =  pgtests.randlett(8)
        self.groupid = 0
        self.pgroupid = 0
        self.orgdrag = ()
        self.others = []
        self.mouse = pggui.Rectangle()
        self.tooltip = "Hello Tooltip"
        DrawObj.globzorder = DrawObj.globzorder + 1
        self.zorder = DrawObj.globzorder
        self.type = ""
        self.mx = [0, 0, 0, 0]      # side markers
        self.rsize = 12             # Marker size

    def dump(self):
        col1 = pggui.float2str(self.col1)
        col2 = pggui.float2str(self.col2)

        rect2 = self.rect.copy()

        #if self.type == "Circ":
        #    print("Half")
        #    rect2.w = rect2.w / 2; rect2.h = rect2.h / 2
        #print("x type: ", self.type, self.rect.dump(), rect2.dump())

        return (self.id, self.text, self.type, str(self.zorder),
                    str(self.groupid), rect2.dump(),
                        str(col1), str(col2), self.others)

    def __str__(self):
        return str(
                (
                self.id, "[" + self.text + "]", self.type, str(self.zorder),
                    str(self.groupid), str(self.rect), str(self.others))
             )

    def expand_size(self, self2):

        neww = self.rect.x + self.rect.w
        if neww > self2.rect.width:
            self2.set_size_request(neww + 20, self2.rect.height)

        newhh = self.rect.y + self.rect.h
        if newhh > self2.rect.height:
            self2.set_size_request(self2.rect.width, newhh + 20)


    def corners(self, self2, rectz, rsize):

        #self2.crh.set_source_rgb(self.col2);
        black = pggui.str2float("#808080")
        self2.crh.set_source_rgb(black)

        self.mx[0] = pggui.Rectangle(rectz.x - rsize/2,
                    rectz.y - rsize/2, rsize, rsize)
        self.mx[1] = pggui.Rectangle(rectz.x + rectz.w - rsize/2,
                    rectz.y - rsize/2, rsize, rsize)
        self.mx[2] = pggui.Rectangle(rectz.x - rsize/2,
                    rectz.y + rectz.h - rsize/2, rsize, rsize)
        self.mx[3] = pggui.Rectangle(rectz.x + rectz.w - rsize/2,
                    rectz.y + rectz.h - rsize/2, rsize, rsize)
        for aa in self.mx:
            if aa:
                self2.crh.rectangle(aa)
        self2.cr.fill()

        # Last one is the handler
        bb = self.mx[3].copy();  bb.resize(-5)
        self2.crh.set_source_rgb(self.col1);
        self2.crh.rectangle(bb)
        self2.cr.fill()

    def hitmarker(self, rectx):

        #print("hit marker", rectx)

        ret = 0 #False
        for aa in range(len(self.mx)):
            if self.mx[aa]:
                if rectx.intersect(self.mx[aa])[0]:
                    ret = aa + 1
                    break
        #if ret:
        #    print ("drawobj  hitmarker", rectx)
        return ret

    def hittest(self, rectx):
        inte = rectx.intersect(self.rect)
        return inte[0]

    def center(self):
        return (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2)

class RectObj(DrawObj):

    ''' Rectangle object '''

    def __init__(self, rect, text, col1, col2, border, fill):

        super(RectObj, self).__init__( rect, text, col1, col2, border, fill)
        self.type = "Rect"

    def draw(self, cr, self2):

        #print("RectObj draw", str(self.rect))

        www = self.rect.w / 50
        if www < .1: www = .1
        cr.set_line_width(www);

        self.expand_size(self2)
        self2.crh.set_source_rgb(self.col1); self2.crh.rectangle(self.rect)
        cr.fill()

        self2.crh.set_source_rgb(self.col2); self2.crh.rectangle(self.rect)
        cr.stroke()

        if self.selected:
            self.corners(self2, self.rect, self.rsize)

        if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            xx, yy = self2.layout.get_pixel_size()
            xxx = self.rect.w / 2 - xx / 2
            yyy = self.rect.h / 2 - yy / 2
            cr.move_to(self.rect.x + xxx, self.rect.y + yyy)
            PangoCairo.show_layout(cr, self2.layout)

        cr.set_line_width(1);


class ImgObj(DrawObj):

    ''' Image object '''

    def __init__(self, rect, text, col1, col2, border, fill):
        super(ImgObj, self).__init__( rect, text, col1, col2, border, fill)

        #self.mx = [0, 0, 0, 0]      # side markers
        #self.rsize = 12             # Marker size
        self.widget = None
        self.pixbuf = None
        self.type   = "Image"
        self.defimage  = os.path.dirname(__file__) + \
                            os.sep + "images/defpic.png"
        #print("image", self.defimage)
        self.image = self.defimage
        self.loadimg()

    def loadimg(self):
        self.widget = Gtk.Image.new_from_file(self.image)
        self.pixbuf = self.widget.get_pixbuf()
        self.pixbuf2 = self.widget.get_pixbuf()
        self.rect.w = self.pixbuf.get_width()
        self.rect.h = self.pixbuf.get_height()

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['widget']
        del state['pixbuf']
        del state['pixbuf2']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.widget  = Gtk.Image.new_from_file(self.image)
        self.pixbuf  = self.widget.get_pixbuf()
        self.pixbuf2 = self.widget.get_pixbuf()

    def draw(self, cr, self2):

        #print("ImgObj draw", str(self.rect))

        ww = self.pixbuf2.get_width()
        hh = self.pixbuf2.get_height()

        # Scale image to new WW / HH
        if self.rect.x > 0 and self.rect.h > 0:

            if self.rect.w != ww or self.rect.h != hh:
                #print("Scale:",     ww, hh, self.rect.w, self.rect.h)
                self.pixbuf2 = self.pixbuf.scale_simple(self.rect.w, self.rect.h,
                                        GdkPixbuf.InterpType.BILINEAR )

            Gdk.cairo_set_source_pixbuf(cr, self.pixbuf2,
                        self.rect.x, self.rect.y)
            cr.paint()

        if self.selected:
            self.corners(self2, self.rect, self.rsize)

        #if self.text:
        #    self2.crh.set_source_rgb(self.col2);
        #    self2.layout.set_text(self.text, len(self.text))
        #    xx, yy = self2.layout.get_pixel_size()
        #    xxx = self.rect.w / 2 - xx / 2
        #    yyy = self.rect.h / 2 - yy / 2
        #    cr.move_to(self.rect.x + xxx, self.rect.y + yyy)
        #    PangoCairo.show_layout(cr, self2.layout)
        #cr.set_line_width(1);


class RoundRectObj(DrawObj):

    ''' RoundRectObj object '''

    def __init__(self, rect, text, col1, col2, border, fill):

        rect2 = pggui.Rectangle(rect[0], rect[1], rect[2], rect[3])

        super(RoundRectObj, self).__init__( rect2, text,
                                    col1, col2, border, fill)
        self.type = "RoundRect"
        self.arr = []

    def hittest(self, rectx):
        inte = rectx.intersect(self.rect)
        return inte[0]

    def draw(self, cr, self2):

        """ Draws a rectangle with rounded corners using cairo. """

        #self.expand_size(self2)

        if self.selected:
            self.corners(self2, self.rect, self.rsize)

        www = self.rect.w / 100
        if www < .1: www = .1
        cr.set_line_width(www);

        self2.crh.set_source_rgb(self.col2);
        self2.crh.roundrect(cr, self.rect)
        cr.stroke()

        self2.crh.set_source_rgb(self.col1);
        self2.crh.roundrect(cr, self.rect)
        cr.fill()

        if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            xx, yy = self2.layout.get_pixel_size()
            xxx = self.rect.w / 2 - xx / 2
            yyy = self.rect.h / 2 - yy / 2
            cr.move_to(self.rect.x + xxx, self.rect.y + yyy)
            PangoCairo.show_layout(cr, self2.layout)

        cr.set_line_width(1);

class LineObj(DrawObj):

    ''' Line object '''

    def __init__(self, rect, text, col1, col2, border, fill):
        super(LineObj, self).__init__( rect, text, col1, col2, border, fill)

        self.type = "Line"

    def draw(self, cr, self2):

        #print("LineObj draw", str(self.rect))

        self.expand_size(self2)
        cr.set_source_rgb(self.col2[0], self.col2[1], self.col2[2])

        cr.move_to(self.rect[0], self.rect[1])
        cr.line_to(self.rect[0] + self.rect[2], self.rect[1] + self.rect[3])
        #cr.fill()
        cr.stroke()

        #self2.crh.set_source_rgb(self.col2); self2.crh.rectangle(self.rect)
        #cr.stroke()

        if self.selected:
            self.corners(self2, self.rect, self.rsize)

        '''if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            xx, yy = self2.layout.get_pixel_size()
            xxx = self.rect.w / 2 - xx / 2
            yyy = self.rect.h / 2 - yy / 2
            cr.move_to(self.rect.x + xxx, self.rect.y + yyy)
            PangoCairo.show_layout(cr, self2.layout)'''

class CurveObj(DrawObj):

    ''' Curves '''

    def __init__(self, rect, text, col1, col2, border, fill):
        super(CurveObj, self).__init__( rect, text, col1, col2, border, fill)

        self.type = "Curve"

    def draw(self, cr, self2):

        #print("CurveObj draw", str(self.rect))

        self.expand_size(self2)
        cr.set_source_rgb(self.col2[0], self.col2[1], self.col2[2])

        cr.move_to(self.rect[0], self.rect[1])
        cr.line_to(self.rect[0] + self.rect[2], self.rect[1] + self.rect[3])
        #cr.fill()
        cr.stroke()

        #self2.crh.set_source_rgb(self.col2); self2.crh.rectangle(self.rect)
        #cr.stroke()

        cent = self.center()
        self.crect = pggui.Rectangle(cent[0], cent[1], self.rsize, self.rsize)

        if self.selected:
            self.corners(self2, self.rect, self.rsize)

        if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            xx, yy = self2.layout.get_pixel_size()
            xxx = self.rect.w / 2 - xx / 2
            yyy = self.rect.h / 2 - yy / 2
            cr.move_to(self.rect.x + xxx, self.rect.y + yyy)
            PangoCairo.show_layout(cr, self2.layout)

        if self.selected:
            self2.crh.set_source_rgb(self.col2);
            self2.crh.rectangle(self.crect)
            cr.stroke()

    def hitmarker(self, rectx):
        ret = 0
        ret = super(CurveObj, self).hitmarker(rectx)
        if not ret:
            if rectx.intersect(self.crect)[0]:
                ret = 5
        #if ret:
        #    print("hit curve",  ret)
        return ret

# ------------------------------------------------------------------------
# Text object

class TextObj(DrawObj):

    ''' Text '''

    def __init__(self, rect, text, col1, col2, border, fill):
        super(TextObj, self).__init__( rect, text, col1, col2, border, fill)

        self.fontstr = "Arial Regular"
        self.fsize = 12
        self.txx = 0 ; self.tyy = 0
        self.type = "Text"
        self.pangolayout = None
        self.skipsize = False

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['pangolayout']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.pangolayout = None

    def center(self):
        return (self.rect.x + self.txx / 2,
                         self.rect.y + self.tyy  / 2)

    def draw(self, cr, self2):

        if not self.pangolayout:
            self.pangolayout = self2.create_pango_layout("a")

        #self.expand_size(self2)

        if self.text:
            self2.crh.set_source_rgb(self.col2);
            fdesc = Pango.FontDescription.from_string(self.fontstr)
            if not self.skipsize:
                self.fsize = max(self.rect.h, 6)
            fdesc.set_size(self.fsize * Pango.SCALE)
            #print("fd", fdesc.to_string(), "sss:", self.fsize)
            self.pangolayout.set_font_description(fdesc)
            self.pangolayout.set_text(self.text, len(self.text))
            self.txx, self.tyy = self.pangolayout.get_pixel_size()

            if self.skipsize:
                #self.rect.w = self.txx
                self.rect.h = self.fsize

            self2.crh.set_source_rgb(self.col2);
            cr.move_to(self.rect.x, self.rect.y)
            PangoCairo.show_layout(cr, self.pangolayout)
            self.skipsize = False

        if self.selected:
            rrr = pggui.Rectangle(self.rect.x, self.rect.y, self.txx, self.tyy)
            self.corners(self2, rrr, self.rsize)

    def hittest(self, rectx):
        recttxt = pggui.Rectangle(self.rect.x, self.rect.y, self.txx, self.tyy)
        inte = rectx.intersect(recttxt)
        return inte[0]

class RombObj(DrawObj):

    ''' Rombus '''

    def __init__(self, rect, text, col1, col2, border, fill):
        super(RombObj, self).__init__( rect, text, col1, col2, border, fill)

        self.type = "Romb"

    def hittest(self, rectx):

        #if aa[0] == CIRC:
        #    rect = pggui.Rectangle(aa[1][0], aa[1][1], aa[1][2], aa[1][2])
        inte = rectx.intersect(self.rect)
        return inte[0]

    def draw(self, cr, self2):

        www = self.rect.w / 40
        if www < .1: www = .1
        cr.set_line_width(www);

        self2.crh.set_source_rgb(self.col1); self2.crh.romb(self.rect)
        cr.fill()

        self2.crh.set_source_rgb(self.col2); self2.crh.romb(self.rect)
        cr.stroke()

        if self.selected:
            self.corners(self2, self.rect, self.rsize)
        if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            xx, yy = self2.layout.get_pixel_size()
            xxx = self.rect.w / 2 - xx / 2
            yyy = self.rect.h / 2 - yy / 2
            cr.move_to(self.rect.x + xxx, self.rect.y + yyy)
            PangoCairo.show_layout(cr, self2.layout)

class CircObj(DrawObj):

    ''' Circle '''

    def __init__(self, rect, text, col1, col2, border, fill):

        rect2 = pggui.Rectangle(rect[0], rect[1], rect[2], rect[3])
        super(CircObj, self).__init__( rect2, text, col1, col2, border, fill)

        self.type = "Circ"

    def hittest(self, rectx):

        ulx = self.rect.x - self.rect.w
        uly = self.rect.y - self.rect.w
        rectc = pggui.Rectangle(ulx, uly, self.rect.w * 2, self.rect.w * 2)
        inte = rectx.intersect(rectc)
        return inte[0]

    def draw(self, cr, self2):

        www = self.rect.w / 40
        if www < .1: www = .1
        cr.set_line_width(www);

        self2.crh.set_source_rgb(self.col1)
        self2.crh.circle(self.rect.x, self.rect.y, self.rect.w)
        cr.fill()

        self2.crh.set_source_rgb(self.col2);
        self2.crh.circle(self.rect.x, self.rect.y, self.rect.w)
        cr.stroke()

        ulx = self.rect.x - self.rect.w
        uly = self.rect.y - self.rect.w

        if self.selected:
            www = 2 * self.rect.w
            rrr = pggui.Rectangle(ulx, uly, www, www)
            self.corners(self2, rrr, self.rsize)

        if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            xx, yy = self2.layout.get_pixel_size()
            cr.move_to(self.rect.x - xx / 2, self.rect.y - yy / 2 )
            PangoCairo.show_layout(cr, self2.layout)

    def center(self):
        return (self.rect.x, self.rect.y)

# ---------------------------------------------------------------

def stroke_dims(arrx):

    ul_x = 10000; ul_y = 10000; lr_x = 0; lr_y = 0
    for aa, bb in arrx:

        ul_x = min(ul_x, aa)
        ul_y = min(ul_y, bb)

        lr_x = max(lr_x, aa)
        lr_y = max(lr_y, bb)

    #print("Stroke dims", ul_x, ul_y, lr_x, lr_y)
    # Correct faulty one
    if ul_x == 10000 or ul_y == 10000:
        ul_x = 10; ul_y = 10; lr_x = 20; lr_y = 20
    return  (ul_x, ul_y, lr_x - ul_x, lr_y - ul_y)

class StrokeObj(DrawObj):

    ''' Stroke '''

    def __init__(self, rect, text, col1, col2, border, fill, arr):

        rect2 = pggui.Rectangle(rect[0], rect[1], rect[2], rect[3])

        super(StrokeObj, self).__init__( rect2, text, col1, col2, border, fill)

        self.type = "Stroke"
        self.arr = self.arr2 = []

        # Convert to relative coords
        for aa, bb in arr:
            self.arr.append((aa - rect[0], bb - rect[1]))

    def draw(self, cr, self2):

        # Calc aspect x y
        org = pggui.Rectangle(stroke_dims(self.arr))

        #self2.crh.set_source_rgb(self.col1)
        self2.crh.set_source_rgb(self.col2);

        init = 0;
        for aa, bb in self.arr:
            aaa = aa; bbb = bb
            try:
                aaa = aa *  self.rect.w / org.w;
                bbb = bb *  self.rect.h / org.h;
            except:
                pass
            if init == 0:
                cr.move_to(aaa + self.rect.x, bbb + self.rect.y)
            else:
                cr.line_to(aaa + self.rect.x, bbb + self.rect.y)
            init += 1
        cr.stroke()

        if self.selected:
            self.corners(self2, self.rect, self.rsize)

        if self.text:
            self2.crh.set_source_rgb(self.col2);
            self2.layout.set_text(self.text, len(self.text))
            cr.move_to(*self.center())
            PangoCairo.show_layout(cr, self2.layout)

    def center(self):
        dims = stroke_dims(self.arr)
        return (self.rect.x + dims[2] / 2, self.rect.y + dims[3] / 2)

# EOF
