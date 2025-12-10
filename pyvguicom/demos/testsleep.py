#!/usr/bin/env python3

import os, sys, time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

from pyvguicom import pgutils

import pgsimp
import pggui
import pggui

timex = time.time()
pggui.usleep(100)
timex2 = time.time()

print("Delay:", timex2-timex)
