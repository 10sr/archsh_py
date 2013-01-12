archsh
======

Shell for archive.

How does it work?
=================

    $ archsh archsh_py.tgz
    Archsh command line for archive
    archsh_py.tgz:/ $ ls
    README.md archsh/   bin/      setup.py
    archsh_py.tgz:/ $ cat README.md # View file content.
    archsh
    ======
    
    Shell for archive.
    archsh_py.tgz:/ $ cd archsh/ # Change directory.
    archsh_py.tgz:/archsh $ ls
    __init__.py archcmd.py  color.py    environ.py  execute.py  handler.py  p7z.py      shell.py    tar.py      zip.py      
    archsh_py.tgz:/archsh $ get e # Completion works.
    environ.py  execute.py
    archsh_py.tgz:/archsh $ get execute.py # Extract file.
    'archsh/execute.py' -> './execute.py'
    archsh_py.tgz:/archsh $ get
    get   getd
    archsh_py.tgz:/archsh $ getd *.py # Extract files with path. Glob also works.
    'archsh/__init__.py' -> './archsh_py-15d0b/archsh/__init__.py'
    'archsh/archcmd.py' -> './archsh_py-15d0b/archsh/archcmd.py'
    'archsh/color.py' -> './archsh_py-15d0b/archsh/color.py'
    'archsh/environ.py' -> './archsh_py-15d0b/archsh/environ.py'
    'archsh/execute.py' -> './archsh_py-15d0b/archsh/execute.py'
    'archsh/handler.py' -> './archsh_py-15d0b/archsh/handler.py'
    'archsh/p7z.py' -> './archsh_py-15d0b/archsh/p7z.py'
    'archsh/shell.py' -> './archsh_py-15d0b/archsh/shell.py'
    'archsh/tar.py' -> './archsh_py-15d0b/archsh/tar.py'
    'archsh/zip.py' -> './archsh_py-15d0b/archsh/zip.py'
    archsh_py.tgz:/archsh $ exit
    Bye!
    $ cd archsh_py-15d0b/ # Files extracted by `getd' command.
    $ ls -R
    .:
    archsh
    
    ./archsh:
    __init__.py  archcmd.py  color.py  environ.py  execute.py  handler.py  p7z.py  shell.py  tar.py  zip.py
    $ exit
    exit
