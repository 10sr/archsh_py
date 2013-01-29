#!/usr/bin/env python3

from archsh.archcmd import ArchCmd
from archsh.execute import Execute
from archsh.environ import Environ

from os.path import isfile, isdir

class Shell():
    def __init__(self, filename):
        if isdir(filename):
            raise OSError("{} is a directory".format(filename))
        elif not isfile(filename):
            raise OSError("{} not found".format(filename))

        self.filename = filename
        self.e = Environ(filename)
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
