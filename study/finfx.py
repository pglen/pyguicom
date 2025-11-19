# ------------------------------------------------------------------------
# Find

def findx(self):

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

    label3 = Gtk.Label(label="   ");  label4 = Gtk.Label(label="   ")
    label5 = Gtk.Label(label="   ");  label6 = Gtk.Label(label="   ")
    label7 = Gtk.Label(label="   ");  label8 = Gtk.Label(label="   ")

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

    label32 = Gtk.Label(label="   ")
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

