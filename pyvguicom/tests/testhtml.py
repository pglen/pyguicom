#!/usr/bin/env python3

'''
  This is a test application for driving the html control;
  It has load / save functionality.
'''
import os, sys, getopt, signal, random, time, warnings

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

sys.path.append(".")

import pggui
import pgutils
import browsewin

warnings.simplefilter("default")

#deftext = "It puzzles me when I see a person lacking fundamentals is \
#  able to amass a fortune to the tune of billions. What is even more \3
#puzziling is that they beleive their own 'BS' and openly flout all."

# The pango example text

deftext = \
'''
Text sizes: <span size="xx-small">tiny</span> <span size="x-small">very small</span> <span size="small">small</span> <span size="medium">normal</span> <span size="large">large</span> <span size="x-large">very large</span> <span size="xx-large">huge</span>
Text <span color="gray">c<span color="green">o</span>l<span color="tomato">o</span>rs</span> and <span background="pink">backgrounds</span>
Colorful <span underline="low" underline-color="blue"><span underline="double" underline-color="red">under</span>lines</span> and <span background="pink"><span underline="error">mo</span><span underline="error" underline-color="green">re</span></span>
Colorful <span strikethrough="true" strikethrough-color="magenta">strikethroughs</span>
Superscripts and subscripts: 𝜀<span rise="-6000" size="x-small" font_desc="italic">0</span> = 𝜔<span rise="8000" size="smaller">𝜔<span rise="14000" size="smaller">𝜔<span rise="20000">.<span rise="23000">.<span rise="26000">.</span></span></span></span></span>
<span letter_spacing="3000">Letterspacing</span>
OpenType font features: <span font_desc="sans regular" font_features="dlig=0">feast</span> versus <span font_desc="sans regular" font_features="dlig=1">feast</span>
Shortcuts: <tt>Monospace</tt> – <b>Bold</b> – <i>Italic</i> – <big>Big</big> – <small>Small</small> – <u>Underlined</u> – <s>Strikethrough</s> – Super<sup>script</sup> – Sub<sub>script</sub>

#'''

ui_def = """
    <ui>
    <menubar name="menubar_main">
        <menu action="menuFile">
        <menuitem action="new" />
        <menuitem action="open" />
        <menuitem action="save" />
        </menu>
        <menu action="menuEdit">
        <menuitem action="cut" />
        <menuitem action="copy" />
        <menuitem action="paste" />
        </menu>
        <menu action="menuInsert">
        <menuitem action="insertimage" />
        </menu>
        <menu action="menuFormat">
        <menuitem action="bold" />
        <menuitem action="italic" />
        <menuitem action="underline" />
        <menuitem action="strikethrough" />
        <separator />
        <menuitem action="font" />
        <menuitem action="color" />
        <separator />
        <menuitem action="justifyleft" />
        <menuitem action="justifyright" />
        <menuitem action="justifycenter" />
        <menuitem action="justifyfull" />
        </menu>
    </menubar>
    <toolbar name="toolbar_main">
        <toolitem action="new" />
        <toolitem action="open" />
        <toolitem action="save" />
        <separator />
        <toolitem action="undo" />
        <toolitem action="redo" />
        <separator />
        <toolitem action="cut" />
        <toolitem action="copy" />
        <toolitem action="paste" />
    </toolbar>
    </ui>
    """

class MainWin(Gtk.Window):

    def __init__(self):

        self.cnt = 0
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)

        self.fname = ""
        self.set_title("Test HtmlEdit")
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        self.set_default_size(800, 600)
        #self.set_default_size(1024, 768)
        self.connect("destroy", self.OnExit)
        #self.connect("key-press-event", self.key_press_event)
        #self.connect("button-press-event", self.button_press_event)

        try:
            self.set_icon_from_file("icon.png")
        except:
            pass

        self.fd = Pango.FontDescription()
        pg = Gtk.Widget.create_pango_context(self)
        myfd = pg.get_font_description()
        mysize = myfd.get_size() / Pango.SCALE
        #print("mysize", mysize)

        self.ui = self.generate_ui()
        warnings.simplefilter("ignore")
        self.toolbar1 = self.ui.get_widget("/toolbar_main")
        self.menubar = self.ui.get_widget("/menubar_main")
        warnings.simplefilter("default")

        self.vbox = Gtk.VBox();
        self.vbox.pack_start(self.menubar, False, False, 0)
        self.vbox.pack_start(self.toolbar1, False, False, 0)
        self.tview = browsewin.browserWin()
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.tview)
        self.vbox.pack_start(self.scroll, 1, 1,2)

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label.new(" "), 1, 1, 0)

        testbutt = Gtk.Button.new_with_mnemonic("   _Import   ")
        testbutt.connect("activate", self.oninp)
        testbutt.connect("pressed", self.oninp)
        hbox.pack_start(testbutt, 0, 0, 0)

        hbox.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        testbutt = Gtk.Button.new_with_mnemonic("   _Export   ")
        testbutt.connect("activate", self.onexp)
        testbutt.connect("pressed", self.onexp)
        hbox.pack_start(testbutt, 0, 0, 0)

        hbox.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        testbutt = Gtk.Button.new_with_mnemonic("   _Test   ")
        testbutt.connect("activate", self.ontest)
        testbutt.connect("pressed", self.ontest)
        hbox.pack_start(testbutt, 0, 0, 0)

        hbox.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        loadbutt = Gtk.Button.new_with_mnemonic("   _Load   ")
        loadbutt.connect("activate", self.onload)
        loadbutt.connect("pressed", self.onload)
        hbox.pack_start(loadbutt, 0, 0, 0)

        hbox.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        savebutt = Gtk.Button.new_with_mnemonic("   _Save   ")
        savebutt.connect("activate", self.onsave)
        savebutt.connect("pressed", self.onsave)
        hbox.pack_start(savebutt, 0, 0, 0)

        hbox.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        butt = Gtk.Button.new_with_mnemonic("   E_xit   ")
        butt.connect("activate", self.OnExit)
        butt.connect("pressed", self.OnExit)
        hbox.pack_start(butt, 0, 0, 0)

        hbox.pack_start(Gtk.Label.new(" "), 0, 0, 0)

        self.vbox.pack_start(hbox, 0, 0, 4)

        self.add(self.vbox)
        self.show_all()


    def generate_ui(self):

        actions = Gtk.ActionGroup(name="Actions")
        warnings.simplefilter("ignore")
        actions.add_actions([
        ("menuFile", None, "_File"),
        ("menuEdit", None, "_Edit"),
        ("menuInsert", None, "_Insert"),
        ("menuFormat", None, "_Format"),

        ("new", Gtk.STOCK_NEW, "_New", None, None, self.on_new),
        ("open", Gtk.STOCK_OPEN, "_Open", None, None, self.on_open),
        ("save", Gtk.STOCK_SAVE, "_Save", None, None, self.on_save),

        ("undo", Gtk.STOCK_UNDO, "_Undo", None, None, self.on_action),
        ("redo", Gtk.STOCK_REDO, "_Redo", None, None, self.on_action),

        ("cut", Gtk.STOCK_CUT, "_Cut", None, None, self.on_action),
        ("copy", Gtk.STOCK_COPY, "_Copy", None, None, self.on_action),
        ("paste", Gtk.STOCK_PASTE, "_Paste", None, None, self.on_paste),

        ("bold", Gtk.STOCK_BOLD, "_Bold", "<ctrl>B", None, self.on_action),
        ("italic", Gtk.STOCK_ITALIC, "_Italic", "<ctrl>I", None, self.on_action),
        ("underline", Gtk.STOCK_UNDERLINE, "_Underline", "<ctrl>U", None, self.on_action),
        ("strikethrough", Gtk.STOCK_STRIKETHROUGH, "_Strike", "<ctrl>T", None, self.on_action),
        ("font", Gtk.STOCK_SELECT_FONT, "Select _Font", "<ctrl>F", None, self.on_select_font),
        ("color", Gtk.STOCK_SELECT_COLOR, "Select _Color", None, None, self.on_select_color),

        ("justifyleft", Gtk.STOCK_JUSTIFY_LEFT, "Justify _Left", None, None, self.on_action),
        ("justifyright", Gtk.STOCK_JUSTIFY_RIGHT, "Justify _Right", None, None, self.on_action),
        ("justifycenter", Gtk.STOCK_JUSTIFY_CENTER, "Justify _Center", None, None, self.on_action),
        ("justifyfull", Gtk.STOCK_JUSTIFY_FILL, "Justify _Full", None, None, self.on_action),

        ("insertimage", "insert-image", "Insert _Image", None, None, self.on_insert_image),
        ("insertlink", "insert-link", "Insert _Link", None, None, self.on_insert_link),
        ])

        actions.get_action("insertimage").set_property("icon-name", "insert-image")
        actions.get_action("insertlink").set_property("icon-name", "insert-link")

        ui = Gtk.UIManager()
        ui.insert_action_group(actions)
        ui.add_ui_from_string(ui_def)
        warnings.simplefilter("default")
        return ui

    def on_action(self, action):
        self.editor.run_javascript("document.execCommand('%s', false, false);" % action.get_name())

    def on_paste(self, action):
        self.editor.execute_editing_command(WebKit2.EDITING_COMMAND_PASTE)

    def on_new(self, action):
        self.editor.load_html("", "file:///")

    def on_select_font(self, action):
        dialog = Gtk.FontChooserDialog("Select a font")
        if dialog.run() == Gtk.ResponseType.OK:
            fname = dialog.get_font_desc().get_family()
            fsize = dialog.get_font_desc().get_size()
            self.editor.run_javascript("document.execCommand('fontname', null, '%s');" % fname)
            self.editor.run_javascript("document.execCommand('fontsize', null, '%s');" % fsize)
        dialog.destroy()

    def on_select_color(self, action):
        dialog = Gtk.ColorChooserDialog("Select Color")
        if dialog.run() == Gtk.ResponseType.OK:
            (r, g, b, a) = dialog.get_rgba()
            color = "#%0.2x%0.2x%0.2x%0.2x" % (
                int(r * 255),
                int(g * 255),
                int(b * 255),
                int(a * 255))
            self.editor.run_javascript("document.execCommand('forecolor', null, '%s');" % color)
        dialog.destroy()

    def on_insert_link(self, action):
        dialog = Gtk.Dialog("Enter a URL:", self, 0,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        entry = Gtk.Entry()
        dialog.vbox.pack_start(entry, False, False, 0)
        dialog.show_all()

        if dialog.run() == Gtk.ResponseType.OK:
            self.editor.run_javascript(
                "document.execCommand('createLink', true, '%s');" % entry.get_text())
        dialog.destroy()

    def on_insert_image(self, action):
        dialog = Gtk.FileChooserDialog("Select an image file", self, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            fn = dialog.get_filename()
            if os.path.exists(fn):
                self.editor.run_javascript(
                "document.execCommand('insertImage', null, '%s');" % fn)
        dialog.destroy()

    def on_open(self, action):
        dialog = Gtk.FileChooserDialog("Select an HTML file", self, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            fn = dialog.get_filename()
            if os.path.exists(fn):
                self.filename = fn
                with open(fn) as fd:
                    self.editor.load_html(fd.read(), "file:///")
        dialog.destroy()

    def on_save(self, action):
        def completion(html, user_data):
            open_mode = user_data
            with open(self.filename, open_mode) as fd:
                fd.write(html)

        if self.filename:
            self.get_html(completion, 'w')
        else:
            dialog = Gtk.FileChooserDialog("Select an HTML file", self, Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            if dialog.run() == Gtk.ResponseType.OK:
                self.filename = dialog.get_filename()
                self.get_html(completion, "w+")
            dialog.destroy()

    def get_html(self, completion_function, user_data):
        def javascript_completion(obj, result, user_data):
            html = self.editor.get_title()
            completion_function(html, user_data)
        self.editor.run_javascript("document.title=document.documentElement.innerHTML;",
                                   None,
                                   javascript_completion,
                                   user_data)

    def oninp(self, butt):
        print("oninp")
        sss = \
        b'GTKTEXTBUFFERCONTENTS-0001\x00\x00\x00\xcc <text_view_markup>\n <tags>\n  ' \
        b'<tag name="bold" priority="7">\n   <attr name="weight" type="gint" value="700" />\n ' \
        b'</tag>\n </tags>\n<text><apply_tag ' \
        b'name="bold">Hello</apply_tag>\n</text>\n</text_view_markup>\n '

    def onexp(self, butt):
        print("onexp")
        #sss = self.tview.ser_buff()
        #print(sss)
        pass

    # Use it to print stuff
    def ontest(self, butt):
        print("ontest")
        pass
        #self.tview.print_tags()

    def onload(self, butt):
        #print("onload", butt)
        self.fname = pggui.opendialog()
        if self.fname:
            fp = open(self.fname, "rb")
            ddd = fp.read()  #.decode("cp437")
            fp.close()
            #self.tview.deser_buff(ddd)

    def onsave(self, butt):
        #print("Save", butt)
        #if not self.tview.textbuffer.get_modified():
        #    pggui.message("\nFile is not modified.", title="File Save")
        #    return
        fname = pggui.savedialog(0)
        #print("got fname", fname)
        if not fname:
            return
        if os.path.isfile(fname):
            resp = pgutils.yes_no_cancel("Overwrite File Prompt",
                        "Overwrite existing file?\n '%s'" % fname, False)
            if resp == Gtk.ResponseType.NO:
                print("not saved")
                return
        #buff  =  self.tview.textbuffer
        #serx = self.tview.ser_buff()
        #print(serx)
        fp = open(fname, "wb")
        fp.write(serx)
        fp.close()
        #self.tview.textbuffer.set_modified(0)

    def OnExit(self, win, arg2 = None):
        resp = None
        #if self.tview.textbuffer.get_modified():
        #    resp = pggui.yes_no_cancel("File modified",
        #    "Save file? \n\n '%s' \n" % self.fname, False)
        #    if resp == Gtk.ResponseType.YES:
        #        #print("saving")
        #        self.onsave(None)

        #print("OnExit", win)
        if resp != Gtk.ResponseType.CANCEL:
            Gtk.main_quit()

if __name__ == '__main__':

    #print("Starting pytextview")
    mainwin = MainWin()

    Gtk.main()

# EOF
