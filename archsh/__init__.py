#!/usr/bin/env python3

"""archsh - shell for Archive

Cd to your archive files and execute commands like ls or less.
"""

from os.path import isfile, isdir

from archsh.archcmd import ArchCmd
from archsh.execute import Execute
from archsh.environ import Environ

class Archsh():
    def __init__(self, filename, type_=None):
        if isdir(filename):
            raise OSError("{} is a directory".format(filename))
        elif not isfile(filename):
            raise OSError("{} not found".format(filename))

        self.filename = filename
        self.e = Environ(filename, type_)
        self.x = Execute(self.e)
        self.c = ArchCmd(self.e, self.x)
        # for e in self.e.list:
        #     print(e)
        return

    def main(self):
        if self.x.handler:
            try:
                self.c.cmdloop()
            finally:
                self.x.finalize()
        else:
            print("No handler found for {}.".format(self.e.file))
        return

def main(filename, type_=None):
    a = Archsh(filename, type_)
    return a.main()

__version__ = "0.0.4"
