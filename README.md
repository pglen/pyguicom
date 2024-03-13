# pyv Common utilites

## Common GUI routines and classes

 These calsses are for python PyGobject (Gtk) development.

These routines are used in several projects. The classes act as a simplification
front end for the PyGtk (PyGobject) classes.

Just a sampler of what is in there (pasted from code, in no particular order):

    class CairoHelper():
    class TextTable(Gtk.Table):
    class TextRow(Gtk.HBox):
    class RadioGroup(Gtk.Frame):
    class Led(Gtk.DrawingArea):
    class SeparatorMenuItem(Gtk.SeparatorMenuItem):
    class Menu():
    class MenuButt(Gtk.DrawingArea):
    class Lights(Gtk.Frame):
    class WideButt(Gtk.Button):
    class ScrollListBox(Gtk.Frame):
    class TextRow(Gtk.HBox):
    class RadioGroup(Gtk.Frame):
    class Led(Gtk.DrawingArea):
    class Lights(Gtk.Frame):
    class FrameTextView(Gtk.TextView):
    class Label(Gtk.Label):
    class Logo(Gtk.VBox):
    class xSpacer(Gtk.HBox):
    class ScrollListBox(Gtk.Frame):
    class ListBox(Gtk.TreeView):

    ... and a lot more ...

## Also includes python / Gtk primitives:

    def get_screen_wh():
    def get_screen_xy():
    def print_exception(xstr):
    def message(strx, parent = None, title = None, icon = Gtk.MessageType.INFO):
    def usleep(msec):
    def tmpname(indir, template):
    def mainloop():
    def time_n2s(ttt):
    def time_s2n(sss):
    def yes_no_cancel(title, message, cancel = True, parent = None):
    def yn_key(win, event, cancel):
    def opendialog(parent=None):
    def savedialog(resp):
    def leadspace(strx):

     ... and a lot more ...

 For instance the Label takes a constructor, and feeds the arguments as
 one would expect.

 Like this:

     def __init__(self, textm = "", widget = None, tooltip=None, font = None):

     The simplification effect allows one to create a label with no arguments,
     and still have a somewhat reasonable outcome. The label example is trivial,
     the simplification takes a new dimension with classed like SimpleTree.

 The defaults are set to a reasonable value, and the named argument can be
set on one line. This makes the code look more compact and maintainable.

## Tests:

 The test utilities can  confirm correct operation; however being a visual
set of classes, the real test is seeing the generated UI.

 See descendent projects for more examples. (pyedpro; pycal; pggui; ...)

Peter Glen

// EOF
