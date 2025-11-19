#!/usr/bin/env python

#pylint: disable=C0103
#pylint: disable=C0209
#pylint: disable=C0321
#pylint: disable=C0116
#pylint: disable=W0301

import os, sys, math, warnings, random, platform

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Pango
from gi.repository import GdkPixbuf

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

    buts =   "Cancel", Gtk.ButtonsType.CANCEL,\
             "Open File", Gtk.ButtonsType.OK
    fc = Gtk.FileChooserDialog(title="Open file", transient_for=parent, \
         action=Gtk.FileChooserAction.OPEN )
    fc.add_buttons(*buts)
    filters = []
    filters.append(makefilter("*.*", "All files (*.*)"))
    filters.append(makefilter("*.html", "HTML files (*.html)"))
    filters.append(makefilter("*.txt", "Text files (*.txt)"))

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
    fc = Gtk.FileChooserDialog(title="Save file as ... ", transient_for=None,
            action=Gtk.FileChooserAction.SAVE)
    fc.add_buttons(*but)
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

'''
for a in (style.base, style.fg, style.bg,
      style.light, style.dark, style.mid,
      style.text, style.base, style.text_aa):
for st in (gtk.STATE_NORMAL, gtk.STATE_INSENSITIVE,
           gtk.STATE_PRELIGHT, gtk.STATE_SELECTED,
           gtk.STATE_ACTIVE):
    a[st] = gtk.gdk.Color(0, 34251, 0)
'''

def version():
    return VERSION

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

def message(strx, parent = None, title = None, icon = Gtk.MessageType.INFO):

    #dialog = Gtk.MessageDialog(parent, Gtk.DialogFlags.DESTROY_WITH_PARENT,
    #    icon, Gtk.ButtonsType.CLOSE, strx)

    dialog = Gtk.MessageDialog(title=title, buttons=Gtk.ButtonsType.CLOSE,
                text=strx, destroy_with_parent=True, modal=True,)

    if parent:
        dialog.set_transient_for(parent)

    if title:
        dialog.set_title(title)
    else:
        dialog.set_title("Message")

    # Close dialog on user response
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.show_all()
    return dialog.run()

def yes_no(messagex, title = "Question", parent=None, default="Yes"):

    dialog = Gtk.MessageDialog(title=title)

    warnings.simplefilter("ignore")
    img = Gtk.Image.new_from_stock(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG)
    dialog.set_image(img)
    warnings.simplefilter("default")

    dialog.set_markup(messagex)

    if default == "Yes":
        dialog.set_default_response(Gtk.ResponseType.YES)
        dialog.add_button("_Yes", Gtk.ResponseType.YES)
        dialog.add_button("_No", Gtk.ResponseType.NO)
    else:
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.add_button("_No", Gtk.ResponseType.NO)
        dialog.add_button("_Yes", Gtk.ResponseType.YES)

    if parent:
        dialog.set_transient_for(parent)

    def _yn_key(win, event, cancel):
        #print("_y_n key", event.keyval)
        if event.keyval == Gdk.KEY_y or \
            event.keyval == Gdk.KEY_Y:
            win.response(Gtk.ResponseType.YES)
        if event.keyval == Gdk.KEY_n or \
            event.keyval == Gdk.KEY_N:
            win.response(Gtk.ResponseType.NO)
        #if cancel:
        #    if event.keyval == Gdk.KEY_c or \
        #        event.keyval == Gdk.KEY_C:
        #        win.response(Gtk.ResponseType.CANCEL)

    dialog.connect("key-press-event", _yn_key, 0)
    # Fri 03.May.2024 destroyed return value
    #dialog.connect("response", lambda d, r: d.destroy())
    dialog.show_all()
    response = dialog.run()
    dialog.destroy()
    #print("response", response, resp2str(response))

    # Convert all other responses to default
    if response == Gtk.ResponseType.REJECT or \
          response == Gtk.ResponseType.CLOSE  or \
             response == Gtk.ResponseType.DELETE_EVENT:
        response = Gtk.ResponseType.NO

        # Cancel means no
        #if default == "Yes":
        #    response = Gtk.ResponseType.YES
        #else:
        #    response = Gtk.ResponseType.NO

    return response

def yes_no_cancel(messagex, title="Question", default="Yes"):

    dialog = Gtk.MessageDialog(title=title)

    if default == "Yes":
        dialog.set_default_response(Gtk.ResponseType.YES)
        dialog.add_button("_Yes", Gtk.ResponseType.YES)
        dialog.add_button("_No", Gtk.ResponseType.NO)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    elif default == "No":
        dialog.set_default_response(Gtk.ResponseType.NO)
        dialog.add_button("_No", Gtk.ResponseType.NO)
        dialog.add_button("_Yes", Gtk.ResponseType.YES)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
    else:
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Yes", Gtk.ResponseType.YES)
        dialog.add_button("_No", Gtk.ResponseType.NO)

    warnings.simplefilter("ignore")
    img = Gtk.Image.new_from_stock(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG)
    dialog.set_image(img)
    warnings.simplefilter("default")
    dialog.set_markup(messagex)

    def _yn_keyc(win, event):
        #print("key:",  event)
        if event.keyval == Gdk.KEY_y or \
            event.keyval == Gdk.KEY_Y:
            win.response(Gtk.ResponseType.YES)
        if event.keyval == Gdk.KEY_n or \
            event.keyval == Gdk.KEY_N:
            win.response(Gtk.ResponseType.NO)
        if event.keyval == Gdk.KEY_c or \
            event.keyval == Gdk.KEY_C:
            win.response(Gtk.ResponseType.CANCEL)

    dialog.connect("key-press-event", _yn_keyc)
    dialog.show_all()
    response = dialog.run()

    # Convert all other responses to cancel
    if  response == Gtk.ResponseType.CANCEL or \
            response == Gtk.ResponseType.REJECT or \
                response == Gtk.ResponseType.CLOSE  or \
                    response == Gtk.ResponseType.DELETE_EVENT:
        response = Gtk.ResponseType.CANCEL

    dialog.destroy()

    #print("yes_no_cancel() result:", response);
    return  response

# EOF
