archsh
======

Shell for archive.

How does it work?
-----------------

    $ archsh archsh_py.tgz
    Archsh command line for archive
    archsh_py.tgz:/ $ # Complete commands by tab.
    EOF    cd     exit   getd   less   more   pwd    sl
    cat    echo   get    help   ls     put    shell  vi
    archsh_py.tgz:/ $ ls
    README.md archsh/   bin/      setup.py
    archsh_py.tgz:/ $ cat README.md # View file content.
    archsh
    ======
    
    Shell for archive.
    archsh_py.tgz:/ $ cd archsh/ # Change directory.
    archsh_py.tgz:/archsh $ ls
    __init__.py color.py    execute.py  p7z.py      tar.py
    archcmd.py  environ.py  handler.py  shell.py    zip.py
    archsh_py.tgz:/archsh $ get e # Complete files.
    environ.py  execute.py
    archsh_py.tgz:/archsh $ get execute.py # Extract files.
    'archsh/execute.py' -> './execute.py'
    archsh_py.tgz:/archsh $ get
    get   getd
    archsh_py.tgz:/archsh $ getd *.py # Extract files with path. And glob works.
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
    archsh_py.tgz:/archsh $ cd
    archsh_py.tgz:/ $ vi
    Modifying file is not supported yet...
    archsh_py.tgz:/archsh $ exit
    Bye!
    $ cd archsh_py-15d0b/
    $ ls -R # Files extracted by `getd' command.
    .:
    archsh
    
    ./archsh:
    __init__.py  color.py	 execute.py  p7z.py    tar.py
    archcmd.py   environ.py  handler.py  shell.py  zip.py
    $

Installation
------------

Execute following command:

    ./setup.py install

Or just create simlink of bin/archsh and put it into your prefered directory
like "$HOME/bin" or "$HOME/.local/bin".

Dependencies
------------

Archsh is tested under python 3.2 and 3.3.

Archive XXX is not supported?
-----------------------------

Please write **handler**! For details read pydoc of archsh.handler .
