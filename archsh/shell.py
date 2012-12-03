#!/usr/bin/env python3

from .prompt import Prompt
from .execute import Execute

class Shell() :
    def __init__(self, archname) :
        self.e = Environ(archname)
        self.p = Prompt(self.e)
        self.x = Execute(self.e)
        for e in self.e.list :
            print(e)
        return

    def main(self) :
        while True :
            self.cmds = self.p.input(self.e)
            if self.cmds != None:
                self.x.run(self.e, self.cmds)
            else :
                break
        return

class Environ() :
    file = ""
    cwd = ""
    list = []
    def __init__(self, archname) :
        self.file = archname
        return
