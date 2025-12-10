#!/usr/bin/env python

import os, sys

sys.path.append(".")

from pyvguicom import pgutils
import comparse

version = "0.00"

optx =  \
[  # option - longname - action - type - defval - help
  ("d", "debug",     "=",    int,   0,   "Debug level (0-9) default=0", ),
  ("f", "fname",     "=",    str,   "untitled", "Filename for out data. defval: untitled"),
  ("t", "trace",     "=",    str,   "None", "Trace flag string.",),
  ("v", "verbose",   "+",    int,   0,   "Increase verbosity level.",),
  ("V", "version",   "b",    bool,  False,   "Show version.",),
]

if __name__ == '__main__':

    comparse.prologue = "Header line."
    comparse.epilogue = "Footer line."
    config = comparse.parse(sys.argv, optx)

    if config.parseerror:
        print(config.parseerror)
        sys.exit(1)
    if config.version:
        print("Version 1.0", end = " ")
        if config.verbose:
            print("built on Sun 23.Nov.2025", end = " ")
        print()
        sys.exit(0)
    if config.help:
        sys.exit(0)

    if config.verbose:
        print("Dumping options:")
        print(config)

    sys.exit(0)

# EOF
