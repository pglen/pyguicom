#!/usr/bin/env python3

import os, string, random, sys, subprocess, time, signal, base64
sys.path.append(".")
sys.path.append("..")

# Set parent as module include path
base = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(base,  '..', '..' ))

def start_server():
    return

    ''' Start server if needed. We start the server on the first test
      (they are executed aplhabettically), and end the server on
      the last test; '''

    if not os.path.isfile(fdirx + lockname):
        print("lockfile", os.path.isfile(fdirx + lockname))
        print("servfile", os.path.isfile(exename))
        print("servfile", exename)
        subprocess.Popen([exename, "-D"])

        #time.sleep(1)
        # wait until it starts .... with a fake connection
        ip = '127.0.0.1'
        hand = pyclisup.CliSup()
        try:
            resp2 = hand.connect(ip, 6666)
        except:
            pass
        hand.client(["quit"], "")

def stop_server():
    return

    # Stop server if needed
    if os.path.isfile(fdirx + lockname):
        print("lockfile", os.path.isfile(fdirx + lockname))
        fp = open(fdirx + lockname)
        buff = fp.read()
        print("buff:", buff)
        fp.close()
        os.kill(int(buff), signal.SIGTERM)
        time.sleep(1)

# Return a random string based upon length
allstr =  string.ascii_lowercase +  string.ascii_uppercase

def randstr(lenx):

    strx = ""
    for aa in range(lenx):
        ridx = random.randint(0, len(allstr)-1)
        rr = allstr[ridx]
        strx += str(rr)
    return strx

# ------------------------------------------------------------------------

test_dir = "test_data"
#if not os.path.isdir(test_dir):
#    os.mkdir(test_dir)

tmpfile = ""

#tmpfile = os.path.splitext(os.path.basename(__file__))[0]
#tmpfile = randstr(8)

# This one will get the last one
for mm in sys.modules:
    if "test_" in mm:
        #print("mod", mm)
        tmpfile = mm
#print("tmpfile", tmpfile)

baseall = os.path.join(test_dir, tmpfile)
#print("baseall", baseall)
#assert 0

# Return a random string based upon length

def randbin(lenx):

    strx = ""
    for aa in range(lenx):
        ridx = random.randint(0, 255)
        strx += chr(ridx)
    return strx.encode("cp437", errors="ignore")

# EOF
