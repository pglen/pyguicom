# pycommon

## Common routines (and classes) for python Gtk (pygobject) development.

 Just a sampler of what is in there (pasted from code):

class CairoHelper():
class   TextTable(Gtk.Table):
class   TextRow(Gtk.HBox):
class   RadioGroup(Gtk.Frame):
class Led(Gtk.DrawingArea):
class   SeparatorMenuItem(Gtk.SeparatorMenuItem):
class Menu():
class MenuButt(Gtk.DrawingArea):
class Lights(Gtk.Frame):
class WideButt(Gtk.Button):
class ScrollListBox(Gtk.Frame):
class   TextRow(Gtk.HBox):
class   RadioGroup(Gtk.Frame):
class Led(Gtk.DrawingArea):
class Lights(Gtk.Frame):
class WideButt(Gtk.Button):
class FrameTextView(Gtk.TextView):
class Label(Gtk.Label):
class Logo(Gtk.VBox):
class xSpacer(Gtk.HBox):
class ScrollListBox(Gtk.Frame):
class ListBox(Gtk.TreeView):

 There is a lot more ...

 These classes act a simplification of PyGtk classes.

 For instance the Label takes a constructor, and feeds the arguments as
 one would expect. Like this:

    def __init__(self, textm = "", widget = None, tooltip=None, font = None):

 The defaults are set to a reasonable value, and the named argument can be
set on one line. This makes the code look compact and maintainable.

 See descendent projects for examples. (pyedpro; pycal; pggui; ...)




