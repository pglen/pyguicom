import os, sys
import setuptools

descx = '''
    These classes are for python PyGobject (Gtk) development. They are used in
    several projects. They act as a simplification front end for the PyGtk / PyGobject
    classes.
    '''

def makelist(droot, exten):
    xlistx = os.listdir(droot)
    xlist = [];
    for aa in xlistx:
        if len(exten):
            if aa[-len(exten):] == exten:
                xlist.append(droot + aa)
        else:
            xlist.append(droot + aa)
    return xlist


doclist = makelist("pyvguicom/docs/", "html")
#print("doclist:", doclist) # ; sys.exit(1)

imglist = makelist("pyvguicom/images/", "png")
#print("imglist:", imglist) # ; sys.exit(1)

#sys.exit(1)

deplist = ["pygobject==3.50.1"] ,

includex = ["*", "pyvguicom", "pyvguicom/demos"]

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
                    'pyvguicom' :   'pyvguicom',
                    #'pyvguicom/docs' :   'pyvguicom/docs',
                    'pyvguicom/demos' :   'pyvguicom/demos',
                    #'pyvguicom/images': 'pyvguicom/images',
                   },
    include_package_data=True,
    package_data = {    "pyvguicom" :  doclist,
                        "pyvguicom" :  imglist,
                   },
    python_requires='>=3',
    install_requires=deplist,
    entry_points={
    },
)

# EOF
