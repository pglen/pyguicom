import os, sys
import setuptools

descx = '''
    These classes are for python PyGobject (Gtk) development. They are used in
    several projects. They act as a simplification front end for the PyGtk / PyGobject
    classes.  See demo subdir for demo and test cases.
    '''

def makelist(droot, dirx, exten):
    ''' Create a list from directories '''
    xlistx = os.listdir(droot); xlist = [];
    for aa in xlistx:
        flag = 0
        if len(exten):
            if aa[-len(exten):] == exten:
                flag = True
        else:
            flag = True
        if flag:
            xlist.append(dirx + aa)
    return xlist

doclist = makelist("pyvguicom/docs/", "docs/", "html")
#print("doclist:", doclist)
imglist = makelist("pyvguicom/images/", "images/", "png")
#print("lists:", doclist + imglist)
#sys.exit(1)

deplist = ["pygobject==3.50.1"] ,
includex = ["*"]

classx = [
          'Development Status :: 6 - Mature',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries',
        ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version number from the file:
fp = open("pyvguicom/pggui.py", "rt")
vvv = fp.read(); fp.close()
loc_vers =  '1.0.0'     # Default
for aa in vvv.split("\n"):
    idx = aa.find("VERSION =")
    if idx == 0:        # At the beginning of line
        try:
            loc_vers = aa.split()[2].replace('"', "")
            break
        except:
            pass
#print("loc_vers:", loc_vers)

setuptools.setup(
    name="pyvguicom",
    version=loc_vers,
    author="Peter Glen",
    author_email="peterglen99@gmail.com",
    description="High power secure 'V' server GUI utility helpers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pglen/pyguicom.git",
    classifiers= classx,
    packages=setuptools.find_packages(include=includex),
    package_dir = {
                    #'pyvguicom'       :   'pyvguicom',
                    #'pyvguicom/demos' :   'pyvguicom/demos',
                   },
    include_package_data=True,
    package_data = {
                    # Note: setup processes only once per dir
                    "pyvguicom"   :    imglist + doclist,
                   },
    python_requires='>=3',
    install_requires=deplist,
    entry_points={
    },
)

# EOF
