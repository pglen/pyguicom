#!/usr/bin/env python3

import os, sys, getopt, signal, select, string, time
import struct, stat, base64, random, zlib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

import pgsimp
import pggui
import pgutils

timex = time.time()
pgutils.usleep(100)
timex2 = time.time()

print("Delay:", timex2-timex)
