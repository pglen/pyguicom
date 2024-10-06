#!/usr/bin/env python

from __future__ import print_function

import os, sys, string, time,  traceback, getopt
import random, glob, warnings

import comline

version = "0.00"

# ------------------------------------------------------------------------

def phelp():

    comline.phelplong()
    sys.exit(0)

    #print()
    #print( "Usage: " + os.path.basename(sys.argv[0]) + " [options]")
    #print()
    #print( "Options:    -d level  - Debug level 0-10")
    #print( "            -p        - Port to use (default: 9999)")
    #print( "            -v        - Verbose")
    #print( "            -V        - Version")
    #print( "            -q        - Quiet")
    #print( "            -h        - Help")
    #print()
    #sys.exit(0)
    #
# ------------------------------------------------------------------------
def pversion(ver = "1.0"):

    comline.pversion(ver)
    #print( os.path.basename(sys.argv[0]), "Version", version)
    #sys.exit(0)

    # option, var_name, initial_val, function, help
optarr = [\
    ["d:",  "debug=",   "pgdebug",  0,      None,     "Debug level. 0=none 10=noisy. Default: 0" ],
    ["p:",  "port=",    "port",     9999,   None,     "Listen on port. Default: 9999"],
    ["v",   "verbose",  "verbose",  0,      None,     "Verbose. Show more info."],
    ["q",   "quiet",    "quiet",    0,      None,     "Quiet. Show less info."],
    ["V",   "version",  None,       None,   pversion, "Print Version string."],
    ["h",   "help",     None,       None,   phelp,    "Show Help. (this screen)"],
    ]

comline.setprog("Custom name")
comline.setargs("[options]")
comline.sethead("Header line.")
comline.setfoot("Footer line.")
conf = comline.ConfigLong(optarr)

if __name__ == '__main__':

    args = conf.comline(sys.argv[1:])
    pversion()
    print()
    phelp()
    sys.exit(0)

# EOF
