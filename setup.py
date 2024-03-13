import setuptools

descx = '''
    These classes are for python PyGobject (Gtk) development. They are used in
    several projects. They act as a simplification front end for the PyGtk / PyGobject
    classes.
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
    description="High power secure server GUI utility helpers.",
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
    package_dir = {
                    'pyvguicom':           'pyvguicom',
                   },
    python_requires='>=3',
    entry_points={
    },
)

# EOF
