#!/usr/bin/env python3

import pytest, os, sys, subprocess, time
from mytest import *

import pgutils

def test_exc(capsys):

    try:
        aa      # Generate Not defined error
    except:
        pgutils.put_exception("Testing")
        #sys.stderr.write("StdError")

    captured = capsys.readouterr()
    #print("cap", captured)

    assert "Context:" in captured.out

def test_timer(capsys):

    res = pgutils.get_time()
    #print(res)
    res2 = pgutils.get_time()
    #print(res2)
    assert res2 > res

def test_oct(capsys):

    qq = pgutils.oct2int("123")
    #print(qq)
    assert qq == 83
    qq2 = pgutils.oct2int("2222")
    #print(qq2)
    assert qq2 == 1170

def test_ascii(capsys):

    aa = pgutils.is_ascii("1234")
    #print(aa)
    assert aa == 0

    aa = pgutils.is_ascii("\xf51234")
    #print(aa)
    assert aa == 1

def test_unescape(capsys):

    sss = "1234\n"
    uu = pgutils.unescape(sss)
    print("'" + uu + "' " + "'" + sss + "'")
    assert uu == sss

def  test_readfile(capsys):

    ff = pgutils.readfile("")
    assert ff == []

    ff = pgutils.readfile("pgutils.py")
    #for aa in ff:
    #    print(aa)
    assert ff

def  test_cleanstr(capsys):

    ff = pgutils.clean_str("pgutils\r\n")
    print(ff)
    #assert 0

def  test_cunescape(capsys):

    ff = pgutils.cunescape("pg\'u \t \b ils\r\n")
    print("cesc", ff)
    assert ff == ff
    #assert 0

def  test_cescape(capsys):

    org = "pg\'u \t \b ils\r\n"
    ff = pgutils.cunescape(org)
    ff2 = pgutils.cescape(ff)
    print("org", ff)
    print("cesc", ff2)
    assert org == ff2

# EOF
