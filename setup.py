import setuptools

descx = '''
        '''

classx = [
          'Development Status :: Mature',
          'Environment :: GUI',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Editors',
          'Topic :: Software Development :: Servers',
        ]

includex = ["*", "pyvguicom"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvguicom",
    version="1.0.0",
    author="Peter Glen",
    author_email="peterglen99@gmail.com",
    description="High power secure server with blockchain backend.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pglen/pyvserv",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(include=includex),

    #scripts = ["pyvserver/pyvserv.py", "pyvclient/pyvcli_cli.py",
    #            "pyvtools/pyvgenkey.py", "pyvtools/pyvgenkeys.py",
    #            "pyvgui/pyvservui.py", "pyvgui/pyvcpanel.py",
    #            "pyvserver/pyvreplic.py",
    #            ],

    package_dir = {
                    'pyvguicom':           'pyvguicom',
                   },

    python_requires='>=3',
    #install_requires=["pyvpacker", "pydbase", "pycryptodome", "pyvecc"],
    entry_points={
        #'console_scripts': [ "pyvserv=pyvserv:mainfunct",
        #                     "pyvreplic=pyvreplic:mainfunct",
        #                     "pyvgenkey=pyvgenkey:mainfunct",
        #                     "pyvgenkeys=pyvgenkeys:mainfunct",
        #                     "pyvservui=pyvservui:mainfunct",
        #                     "pyvcpanel=pyvcpanel:mainfunct",
        #                     "pyvcli_cli=pyvcli_cli:mainfunct",
        #    ],
    },
)

# EOF
