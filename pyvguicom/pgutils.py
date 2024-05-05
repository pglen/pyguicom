#!/usr/bin/python

# pylint: disable=C0103
# pylint: disable=C0209
# pylint: disable=C0321

import os, sys, getopt, string,  math
import random, time, traceback, stat
import platform

#import warmings

if sys.version_info.major < 3:
    pass
else:
    import inspect
    if inspect.isbuiltin(time.process_time):
        time.clock = time.process_time

''' General utility fiunctions '''

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

# ------------------------------------------------------------------------
# Resolve path name

def respath(fname):

    try:
        ppp = str.split(os.environ['PATH'], os.pathsep)
        for aa in ppp:
            ttt = aa + os.sep + fname
            if os.path.isfile(str(ttt)):
                return ttt
    except:
        print ("Cannot resolve path", fname, sys.exc_info())
    return None

# ------------------------------------------------------------------------
# Color conversions

def str2col(strx):
    ccc = str2float(strx)
    return float2col(ccc)

def str2float( col):
    return ( float(int(col[1:3], base=16)) / 256,
                    float(int(col[3:5], base=16)) / 256, \
                        float(int(col[5:7], base=16)) / 256 )

def float2col(col):
    aa = min(col[0], 1.)
    bb = min(col[1], 1.)
    cc = min(col[2], 1.)
    return Gdk.Color(aa * 65535, bb * 65535, cc * 65535)

def float2str(col):
    aa = min(col[0], 1.)
    bb = min(col[1], 1.)
    cc = min(col[2], 1.)
    strx = "#%02x%02x%02x" % (aa * 256,  \
                        bb * 256, cc * 256)
    return strx

def col2float(col):
    rrr = [float(col.red) / 65535,
            float(col.green) / 65535,
                float(col.blue) / 65535]
    return rrr

def rgb2str(icol):
    strx = "#%02x%02x%02x" % (int(icol.red) & 0xff,  \
                        int(icol.green) & 0xff, int(icol.blue) & 0xff)
    return strx

def col2str(icol):
    strx = "#%02x%02x%02x" % (int(icol.red / 255),  \
                        int(icol.green / 255), int(icol.blue / 255))
    return strx

def rgb2col(icol):
    #print "rgb2col", icol
    col = [0, 0, 0]
    col[0] = float(icol.red) / 256
    col[1] = float(icol.green) / 256
    col[2] = float(icol.blue) / 256
    return col

def put_debug2(xstr):
    try:
        if os.isatty(sys.stdout.fileno()):
            print( xstr)
        else:
            #syslog.syslog(xstr)
            pass
            print(xstr, file=sys.stderr)

    except:
        print( "Failed on debug output.")
        print( sys.exc_info())

def put_exception(xstr):

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                cumm += "File: " + os.path.basename(aa[0]) + \
                        "  Line: " + str(aa[1]) + "\n" +  \
                        "    Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print( "Could not print trace stack. ", sys.exc_info())

    print(cumm)
    #syslog.syslog("%s %s %s" % (xstr, a, b))

def decode_bits(numx):
    mask = 0x80
    retx = ""
    for aa in range(8):
        strx = "0"
        if numx & mask:
            strx = "1"
        retx += "B%d=%s  " % (7-aa, strx)
        if aa == 3:
            retx += "\r"
        mask >>= 1

    return retx

# ------------------------------------------------------------------------
# Remove non printables

def clean_str(strx):

    stry = ""
    for aa in range(len(strx)):
        if strx[aa] == '\r':
            stry += "\\r"
        elif strx[aa] == '\n':
            stry += "\\n"
        elif strx[aa] == '\0':
            stry += "\\0"
        else:
            stry += strx[aa]
    return stry

def clean_str2(strx):
    stry = ""
    skip = False
    for aa in range(len(strx)):
        if skip:
            skip = False
            continue
        if strx[aa] == '\\' and strx[aa+1] == 'r':
            skip = True
        if strx[aa] == '\\' and strx[aa+1] == 'n':
            skip = True
        if strx[aa] == '\\' and strx[aa+1] == '0':
            skip = True
            pass
        else:
            stry += strx[aa]
    return stry

# This is crafted to Py2 so has clock with the same name

start_time = time.clock()

def  get_time():

    global start_time
    if sys.version_info.major < 3:
        return time.clock()  - start_time
    else:
        return time.process_time()

def get_realtime():

    frac = math.modf(float(get_time()))
    zzz = "%.02f" % frac[0]
    sss = "%s%s" % (time.strftime("%02I:%02M:%02S"), zzz[1:])
    return sss

# Get a list of ports

'''
def serial_ports():

    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """

    ports = []
    if sys.platform.startswith('win'):
        ports2 = serial.tools.list_ports.comports()
        for aa in ports2:
            ports.append(aa[0])
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyU[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        # rely on serial module
        ports2 = serial.tools.list_ports.comports()
        for aa in ports2:
            ports.append(aa[0])
        #raise EnvironmentError('Unsupported platform')

    #print ("ports", ports)
    result = []
    for port in ports:
        try:
            # no testing performed any more
            #s = serial.Serial(port)
            #s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    #print ("result", result)
    return result
'''

# ------------------------------------------------------------------------
# Convert octal string to integer

def oct2int(strx):
    retx = 0
    for aa in strx:
        num = ord(aa) - ord("0")
        if num > 7 or num < 0:
            break
        retx <<= 3; retx += num
    #print "oct:", strx, "int:", retx
    return retx

# ------------------------------------------------------------------------
# Convert unicode sequence to unicode char

def uni(xtab):

    #print str.format("{0:b}",  xtab[0])
    try:
        unichr
    except NameError:
        unichr = chr

    cc = 0
    try:
        if xtab[0] & 0xe0 == 0xc0:  # two numbers
            cc = (xtab[0] & 0x1f) << 6
            cc += (xtab[1] & 0x3f)
        elif xtab[0] & 0xf0 == 0xe0: # three numbers
            cc = (xtab[0] & 0x0f) << 12
            cc += (xtab[1] & 0x3f) << 6
            cc += (xtab[2] & 0x3f)
        elif xtab[0] & 0xf8 == 0xf0: # four numbers
            cc = (xtab[0] & 0x0e)  << 18
            cc += (xtab[1] & 0x3f) << 12
            cc += (xtab[2] & 0x3f) << 6
            cc += (xtab[3] & 0x3f)
        elif xtab[0] & 0xfc == 0xf8: # five numbers
            cc = (xtab[0] & 0x03)  << 24
            cc += (xtab[1] & 0x3f) << 18
            cc += (xtab[2] & 0x3f) << 12
            cc += (xtab[3] & 0x3f) << 6
            cc += (xtab[4] & 0x3f)
        elif xtab[0] & 0xfe == 0xf8: # six numbers
            cc = (xtab[0] & 0x01)  << 30
            cc += (xtab[1] & 0x3f) << 24
            cc += (xtab[2] & 0x3f) << 18
            cc += (xtab[3] & 0x3f) << 12
            cc += (xtab[4] & 0x3f) << 6
            cc += (xtab[5] & 0x3f)

        ccc = unichr(cc)
    except:
        pass

    return ccc

def is_ascii(strx):

    pos = 0; lenx = len(strx)
    while True:
        if pos >= lenx:
            break

        chh = strx[pos]
        #print (ord(chh))
        if ord(chh) > 127:
            #print (ord(chh))
            if pos == 0: pos += 1
            return pos
        pos+= 1

    return 0

def kill_non_ascii(strx):

    str2 = ""
    pos = 0; lenx = len(strx)
    while True:
        if pos >= lenx:
            break

        chh = strx[pos]
        #print (ord(chh))
        if ord(chh) <= 127:
            str2 += chh
        else:
            str2 += "*"
        pos+= 1

    return str2

# ------------------------------------------------------------------------
# Unescape unicode into displayable sequence

xtab = []; xtablen = 0

def unescape(strx):

    #print " x[" + strx + "]x "

    global xtab, xtablen
    retx = u""; pos = 0; lenx = len(strx)

    while True:
        if pos >= lenx:
            break

        chh = strx[pos]

        if chh == '\\':
            #print "backslash", strx[pos:]
            pos2 = pos + 1; strx2 = ""
            while True:
                if pos2 >= lenx:
                    # See if we accumulated anything
                    if strx2 != "":
                        xtab.append(oct2int(strx2))
                    if len(xtab) > 0:
                        #print "final:", xtab
                        if xtablen == len(xtab):
                            retx += uni(xtab)
                            xtab = []; xtablen = 0
                    pos = pos2 - 1
                    break
                chh2 = strx[pos2]
                if chh2  >= "0" and chh2 <= "7":
                    strx2 += chh2
                else:
                    #print "strx2: '"  + strx2 + "'"
                    if strx2 != "":
                        octx = oct2int(strx2)
                        if xtablen == 0:
                            if octx & 0xe0 == 0xc0:
                                #print "two ",str.format("{0:b}", octx)
                                xtablen = 2
                                xtab.append(octx)
                            elif octx & 0xf0 == 0xe0: # three numbers
                                #print "three ",str.format("{0:b}", octx)
                                xtablen = 3
                                xtab.append(octx)
                            elif octx & 0xf8 == 0xf0: # four numbers
                                print("four ",str.format("{0:b}", octx))
                                xtablen = 4
                                xtab.append(octx)
                            elif octx & 0xfc == 0xf8: # five numbers
                                print("five ",str.format("{0:b}", octx))
                                xtablen = 5
                                xtab.append(octx)
                            elif octx & 0xfe == 0xfc: # six numbers
                                print("six ",str.format("{0:b}", octx))
                                xtablen = 6
                                xtab.append(octx)
                            else:
                                #print "other ",str.format("{0:b}", octx)
                                #retx += unichr(octx)
                                retx += chr(octx)
                        else:
                            xtab.append(octx)
                            #print "data ",str.format("{0:b}", octx)
                            if xtablen == len(xtab):
                                retx += uni(xtab)
                                xtab = []; xtablen = 0

                    pos = pos2 - 1
                    break
                pos2 += 1
        else:

            if xtablen == len(xtab) and xtablen != 0:
                retx += uni(xtab)
            xtab=[]; xtablen = 0

            try:
                retx += chh
            except:
                pass
        pos += 1

    #print "y[" + retx + "]y"
    return retx

# ------------------------------------------------------------------------
# Give the user the usual options for true / false - 1 / 0 - y / n

def isTrue(strx):
    if strx == "1": return True
    if strx == "0": return False
    uuu = strx.upper()
    if uuu == "TRUE": return True
    if uuu == "FALSE": return False
    if uuu == "Y": return True
    if uuu == "N": return False
    return False

# ------------------------------------------------------------------------
# Return True if file exists

def isfile(fname):

    try:
        ss = os.stat(fname)
    except:
        return False

    if stat.S_ISREG(ss[stat.ST_MODE]):
        return True
    return False

def put_exception2_old(xstr):

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print( "Could not print trace stack. ", sys.exc_info())

    put_debug2(cumm)
    #syslog.syslog("%s %s %s" % (xstr, a, b))

# Create a one way hash of a name. Not cryptographically secure,
# but it can make a good unique name in hex.

def hash_name(strx):

    lenx = len(strx);  hashx = int(0)
    for aa in strx:
        bb = ord(aa)
        hashx +=  int((bb << 12) + bb)
        hashx &= 0xffffffff
        hashx = int(hashx << 8) + int(hashx >> 8)
        hashx &= 0xffffffff

    return "%x" % hashx

# Expand tabs in string
def untab_str(strx, tabstop = 4):
    res = ""; idx = 0; cnt = 0
    xlen = len(strx)
    while True:
        if idx >= xlen: break
        chh = strx[idx]
        if  chh == "\t":
            # Generate string
            spaces = tabstop - (cnt % tabstop)
            ttt = ""
            for aa in range(spaces):
                ttt += " "
            res += ttt
            cnt += spaces
        else:
            cnt += 1
            res += chh
        idx += 1
    return res

# ------------------------------------------------------------------------
# Get am pm version of a number

def ampmstr(bb):

    dd = "AM"
    if bb == 12:
        dd = "PM"
    elif bb > 12:
        bb -= 12
        dd = "PM"
    return "%02d %s" % (bb, dd)

# It's totally optional to do this, you could just manually insert icons
# and have them not be themeable, especially if you never expect people
# to theme your app.

def register_stock_icons():
    ''' This function registers our custom toolbar icons, so they
        can be themed.
    '''
    #items = [('demo-gtk-logo', '_GTK!', 0, 0, '')]
    # Register our stock items
    #Gtk.stock_add(items)

    # Add our custom icon factory to the list of defaults
    factory = Gtk.IconFactory()
    factory.add_default()

    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')

    #print( img_path)
    try:
        #pixbuf = Gdk.pixbuf_new_from_file(img_path)
        # Register icon to accompany stock item

        # The gtk-logo-rgb icon has a white background, make it transparent
        # the call is wrapped to (gboolean, guchar, guchar, guchar)
        #transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
        #icon_set = Gtk.IconSet(transparent)
        #factory.add('demo-gtk-logo', icon_set)
        pass
    except GObject.GError as error:
        #print( 'failed to load GTK logo ... trying local')
        try:
            #img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
            xbuf = Gdk.pixbuf_new_from_file('gtk-logo-rgb.gif')
            #Register icon to accompany stock item
            #The gtk-logo-rgb icon has a white background, make it transparent
            #the call is wrapped to (gboolean, guchar, guchar, guchar)
            transparent = xbuf.add_alpha(True, chr(255), chr(255),chr(255))
            icon_set = Gtk.IconSet(transparent)
            factory.add('demo-gtk-logo', icon_set)

        except GObject.GError as error:
            print('failed to load GTK logo for toolbar')

# ------------------------------------------------------------------------
# Let the higher level deal with errors.

def  readfile(strx, sep = None):

    text = []

    if strx == "":
        return text

    # Now read and parse
    f = open(strx, "rb");  buff2 = f.read();  f.close()
    if sys.version_info.major < 3:
        buff = buff2
    else:
        try:
            buff = buff2.decode('UTF-8')
        except UnicodeDecodeError:
            buff = buff2.decode('cp437')

    buff2 = ""

    if not sep:
        # Deteremine separator, use a partial length search
        if buff.find("\r\n", 0, 300) >= 0:
            sep = "\r\n"
        elif buff.find("\n\r", 0, 300) >= 0:
            sep = "\n\r"
        elif buff.find("\r", 0, 300) >= 0:
            sep = "\r"
        else:
            sep = "\n"

    text2 = str.split(buff, sep)

    #if "Makefile" in strx:
    #    print(strx, "sep: '"+ sep + "'", ord(sep[0]), ord(sep[1]))

    # Clean out spuriously occurring \r and \n
    # Example: ST Microelectronics Makefiles

    text = []
    for aa in text2:
        #print("'%s\n" % aa)
        bb = aa.replace("\r", "")
        cc = bb.replace("\n", "")
        text.append(cc)
    #text2 = []

    return text

# ------------------------------------------------------------------------
# Handle command line. Interpret optarray and decorate the class
# This allows a lot of sub utils to have a common set of options.

class Config:

    def __init__(self, optarr):
        self.optarr = optarr
        self.verbose = False
        self.debug = False

    def comline(self, argv):
        optletters = ""
        for aa in self.optarr:
            optletters += aa[0]
        #print( optletters    )
        # Create defaults:
        err = 0
        for bb in range(len(self.optarr)):
            if self.optarr[bb][1]:
                # Coerse type
                if type(self.optarr[bb][2]) == type(0):
                    self.__dict__[self.optarr[bb][1]] = int(self.optarr[bb][2])
                if type(self.optarr[bb][2]) == type(""):
                    self.__dict__[self.optarr[bb][1]] = str(self.optarr[bb][2])
        try:
            opts, args = getopt.getopt(argv, optletters)
        #except getopt.GetoptError, err:
        except:
            print( "Invalid option(s) on command line:", err)
            #support.put_exception("comline")
            return ()

        #print( "opts", opts, "args", args)
        for aa in opts:
            for bb in range(len(self.optarr)):
                if aa[0][1] == self.optarr[bb][0][0]:
                    #print( "match", aa, self.optarr[bb])
                    if len(self.optarr[bb][0]) > 1:
                        #print( "arg", self.optarr[bb][1], aa[1])
                        if self.optarr[bb][2] != None:
                            if type(self.optarr[bb][2]) == type(0):
                                self.__dict__[self.optarr[bb][1]] = int(aa[1])
                            if type(self.optarr[bb][2]) == type(""):
                                self.__dict__[self.optarr[bb][1]] = str(aa[1])
                    else:
                        #print( "set", self.optarr[bb][1], self.optarr[bb][2])
                        if self.optarr[bb][2] != None:
                            self.__dict__[self.optarr[bb][1]] = 1
                        #print( "call", self.optarr[bb][3])
                        if self.optarr[bb][3] != None:
                            self.optarr[bb][3]()
        return args

def  about(progname, verstr = "1.0.0", imgfile = "icon.png"):

    ''' Show About dialog: '''

    dialog = Gtk.AboutDialog()
    dialog.set_name(progname)

    dialog.set_version(verstr)
    gver = (Gtk.get_major_version(), \
                        Gtk.get_minor_version(), \
                            Gtk.get_micro_version())

    dialog.set_position(Gtk.WindowPosition.CENTER)
    #dialog.set_transient_for(pedconfig.conf.pedwin.mywin)

    #"\nRunning PyGObject %d.%d.%d" % GObject.pygobject_version +\

    ddd = os.path.join(os.path.dirname(__file__))

    # GLib.pyglib_version
    vvv = gi.version_info
    comm = \
        "Running PyGtk %d.%d.%d" % vvv +\
        "\non GTK %d.%d.%d" % gver +\
        "\nRunning Python %s" % platform.python_version() +\
        "\non %s %s" % (platform.system(), platform.release()) +\
        "\nExe Path:\n%s" % os.path.realpath(ddd)

    dialog.set_comments(comm)
    dialog.set_copyright(progname + " Created by Peter Glen.\n"
                          "Project is in the Public Domain.")
    dialog.set_program_name(progname)
    img_path = os.path.join(os.path.dirname(__file__), imgfile)

    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        #print "loaded pixbuf"
        dialog.set_logo(pixbuf)

    except:
        print("Cannot load logo for about dialog", img_path)
        print(sys.exc_info())

    #dialog.set_website("")

    ## Close dialog on user response
    dialog.connect ("response", lambda d, r: d.destroy())
    dialog.connect("key-press-event", _about_key)

    dialog.show()

def _about_key(win, event):
    #print "about_key", event
    if  event.type == Gdk.EventType.KEY_PRESS:
        if event.keyval == Gdk.KEY_x or event.keyval == Gdk.KEY_X:
            if event.state & Gdk.ModifierType.MOD1_MASK:
                win.destroy()

# ------------------------------------------------------------------------
# Show a regular message:
#
#def message3(strx, title = None):
#
#    #print("called: message()", strx)
#
#    icon = Gtk.STOCK_INFO
#    dialog = Gtk.MessageDialog(buttons=Gtk.ButtonsType.CLOSE,
#                               message_type=Gtk.MessageType.INFO)
#    dialog.props.text = strx
#    #dialog.set_transient_for()
#    if title:
#        dialog.set_title(title)
#    else:
#        dialog.set_title("PyEdPro")
#    dialog.set_position(Gtk.WindowPosition.CENTER)
#    # Close dialog on user response
#    dialog.connect("response", lambda d, r: d.destroy())
#    dialog.show()
#    dialog.run()

# -----------------------------------------------------------------------
# Call func with all processes, func called with stat as its argument
# Function may return True to stop iteration

def withps(func, opt = None):

    ret = False
    dl = os.listdir("/proc")
    for aa in dl:
        fname = "/proc/" + aa + "/stat"
        if os.path.isfile(fname):
            ff = open(fname, "r").read().split()
            ret = func(ff, opt)
        if ret:
            break
    return ret

# ------------------------------------------------------------------------
# Find

def find(self):

    head = "Find in text"

    dialog = Gtk.Dialog(head,
                   None,
                   Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
                   (Gtk.STOCK_CANCEL, Gtk.RESPONSE_REJECT,
                    Gtk.STOCK_OK, Gtk.RESPONSE_ACCEPT))
    dialog.set_default_response(Gtk.RESPONSE_ACCEPT)

    try:
        dialog.set_icon_from_file("epub.png")
    except:
        print ("Cannot load find dialog icon", sys.exc_info())

    self.dialog = dialog

    label3 = Gtk.Label("   ");  label4 = Gtk.Label("   ")
    label5 = Gtk.Label("   ");  label6 = Gtk.Label("   ")
    label7 = Gtk.Label("   ");  label8 = Gtk.Label("   ")

    #warmings.simplefilter("ignore")
    entry = Gtk.Entry()
    #warmings.simplefilter("default")
    entry.set_text(self.oldfind)

    entry.set_activates_default(True)

    dialog.vbox.pack_start(label4)

    hbox2 = Gtk.HBox()
    hbox2.pack_start(label6, False)
    hbox2.pack_start(entry)
    hbox2.pack_start(label7, False)

    dialog.vbox.pack_start(hbox2)

    dialog.checkbox = Gtk.CheckButton("Search _Backwards")
    dialog.checkbox2 = Gtk.CheckButton("Case In_sensitive")
    dialog.vbox.pack_start(label5)

    hbox = Gtk.HBox()
    #hbox.pack_start(label1);  hbox.pack_start(dialog.checkbox)
    #hbox.pack_start(label2);  hbox.pack_start(dialog.checkbox2)
    hbox.pack_start(label3)
    dialog.vbox.pack_start(hbox)
    dialog.vbox.pack_start(label8)

    label32 = Gtk.Label("   ")
    hbox4 = Gtk.HBox()

    hbox4.pack_start(label32)
    dialog.vbox.pack_start(hbox4)

    dialog.show_all()
    response = dialog.run()
    self.srctxt = entry.get_text()

    dialog.destroy()

    if response != Gtk.RESPONSE_ACCEPT:
        return None

    return self.srctxt, dialog.checkbox.get_active(), \
                dialog.checkbox2.get_active()

disp = Gdk.Display.get_default()
scr = disp.get_default_screen()

#print( "num_mon",  scr.get_n_monitors()    )
#for aa in range(scr.get_n_monitors()):
#    print( "mon", aa, scr.get_monitor_geometry(aa);)

# ------------------------------------------------------------------------
# Get current screen (monitor) width and height

def get_screen_wh():

    ptr = disp.get_pointer()
    mon = scr.get_monitor_at_point(ptr[1], ptr[2])
    geo = scr.get_monitor_geometry(mon)
    www = geo.width; hhh = geo.height
    if www == 0 or hhh == 0:
        www = Gdk.get_screen_width()
        hhh = Gdk.get_screen_height()
    return www, hhh

# ------------------------------------------------------------------------
# Get current screen (monitor) upper left corner xx / yy

def get_screen_xy():

    ptr = disp.get_pointer()
    mon = scr.get_monitor_at_point(ptr[1], ptr[2])
    geo = scr.get_monitor_geometry(mon)
    return geo.x, geo.y

# ------------------------------------------------------------------------
# Print( an exception as the system would print it)

def print_exception(xstr):
    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print("Could not print trace stack. ", sys.exc_info())
    print( cumm)

# -----------------------------------------------------------------------
# Sleep just a little, but allow the system to breed

def  usleep(msec):

    if sys.version_info[0] < 3 or \
        (sys.version_info[0] == 3 and sys.version_info[1] < 3):
        timefunc = time.clock
    else:
        timefunc = time.process_time

    got_clock = timefunc() + float(msec) / 1000
    #print( got_clock)
    while True:
        if timefunc() > got_clock:
            break
        #print ("Sleeping")
        Gtk.main_iteration_do(False)

# ------------------------------------------------------------------------
# Create temporary file, return name. Empty string ("") if error.

def tmpname(indir, template):

    fname = ""
    if not os.access(indir, os.W_OK):
        print( "Cannot access ", indir)
        return fname

    cnt = 1
    while True:
        tmp = indir + "/" + template + "_" + str(cnt)
        if not os.access(tmp, os.R_OK):
            fname = tmp
            break
        # Safety valve
        if cnt > 10000:
            break
    return fname

# ------------------------------------------------------------------------
# Execute man loop

def mainloop():
    while True:
        ev = Gdk.event_peek()
        #print( ev)
        if ev:
            if ev.type == Gdk.EventType.DELETE:
                break
            if ev.type == Gdk.EventType.UNMAP:
                break
        if Gtk.main_iteration_do(True):
            break

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

# Time to str and str to time

def time_n2s(ttt):
    sss = time.ctime(ttt)
    return sss

def time_s2n(sss):
    rrr = time.strptime(sss)
    ttt = time.mktime(rrr)
    return ttt

def opendialog(parent=None):

    # We create an array, so it is passed around by reference
    fname = [""]

    def makefilter(mask, name):
        filter =  Gtk.FileFilter.new()
        filter.add_pattern(mask)
        filter.set_name(name)
        return filter

    def done_open_fc(win, resp, fname):
        #print "done_open_fc", win, resp
        if resp == Gtk.ButtonsType.OK:
            fname[0] = win.get_filename()
            if not fname[0]:
                #print "Must have filename"
                pass
            elif os.path.isdir(fname[0]):
                os.chdir(fname[0])
                win.set_current_folder(fname[0])
                return
            else:
                #print("OFD", fname[0])
                pass
        win.destroy()

    but =   "Cancel", Gtk.ButtonsType.CANCEL,\
            "Open File", Gtk.ButtonsType.OK

    fc = Gtk.FileChooserDialog("Open file", parent, \
         Gtk.FileChooserAction.OPEN  \
        , but)

    filters = []
    filters.append(makefilter("*.mup", "MarkUp files (*.py)"))
    filters.append(makefilter("*.*", "All files (*.*)"))

    if filters:
        for aa in filters:
            fc.add_filter(aa)

    fc.set_default_response(Gtk.ButtonsType.OK)
    fc.set_current_folder(os.getcwd())
    fc.connect("response", done_open_fc, fname)
    #fc.connect("current-folder-changed", self.folder_ch )
    #fc.set_current_name(self.fname)
    fc.run()
    #print("OFD2", fname[0])
    return fname[0]

def savedialog(resp):

    #print "File dialog"
    fname = [""]   # So it is passed around as a reference

    def makefilter(mask, name):
        filterx =  Gtk.FileFilter.new()
        filterx.add_pattern(mask)
        filterx.set_name(name)
        return filterx

    def done_fc(win, resp, fname):
        #print( "done_fc", win, resp)
        if resp == Gtk.ResponseType.OK:
            fname[0] = win.get_filename()
            if not fname[0]:
                print("Must have filename")
            else:
                pass
        win.destroy()

    but =   "Cancel", Gtk.ResponseType.CANCEL,   \
                    "Save File", Gtk.ResponseType.OK
    fc = Gtk.FileChooserDialog("Save file as ... ", None,
            Gtk.FileChooserAction.SAVE, but)

    #fc.set_do_overwrite_confirmation(True)

    filters = []
    filters.append(makefilter("*.mup", "MarkUp files (*.py)"))
    filters.append(makefilter("*.*", "All files (*.*)"))

    if filters:
        for aa in filters:
            fc.add_filter(aa)

    fc.set_current_name(os.path.basename(fname[0]))
    fc.set_current_folder(os.path.dirname(fname[0]))
    fc.set_default_response(Gtk.ResponseType.OK)
    fc.connect("response", done_fc, fname)
    fc.run()
    return fname[0]

# ------------------------------------------------------------------------

def leadspace(strx):

    ''' Count lead spaces '''

    cnt = 0
    for aa in range(len(strx)):
        bb = strx[aa]
        if bb == " ":
            cnt += 1
        elif bb == "\t":
            cnt += 1
        elif bb == "\r":
            cnt += 1
        elif bb == "\n":
            cnt += 1
        else:
            break
    return cnt

def wrapscroll(what):

    scroll2 = Gtk.ScrolledWindow()
    scroll2.add(what)
    frame2 = Gtk.Frame()
    frame2.add(scroll2)
    return frame2

if __name__ == '__main__':
    print("This file was not meant to run directly")

# EOF
