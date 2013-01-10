#!/usr/bin/env python3

from .archcmd import ArchCmd
from .execute import Execute
from .environ import Environ

from os.path import isfile, isdir

class Shell():
    def __init__(self, archname):
        if isdir(archname):
            raise OSError("{} is a directory".format(archname))
        elif not isfile(archname):
            raise OSError("{} not found".format(archname))

        self.e = Environ(archname)
        self.x = Execute(self.e)
        self.c = ArchCmd(self.e, self.x)
        # for e in self.e.list:
        #     print(e)
        return

    def main(self):
        if self.x.handler:
            self.c.cmdloop()
        else:
            print("No handler found for {}.".format(self.e.file))
        return
