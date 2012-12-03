#!/usr/bin/env python3

from .prompt import Prompt
from .execute import Execute

class Shell() :
    def __init__(self, archname) :
        self.e = Environ(archname)
        self.p = Prompt(self.e)
        self.x = Execute(self.e)
        # for e in self.e.list :
        #     print(e)
        return

    def main(self) :
        while True :
            self.cmds = self.p.input()
            if self.cmds != None:
                self.x.run(self.cmds)
            else :
                break
        return

class Environ() :
    file = ""                   # filename of archive
    cwd = ""                    # cwd without leading "/"
    list = []                   # all file list, do not update while ro
    child = []                  # list of file under current dir
    current = []                # file list current dir contains
    def __init__(self, archname) :
        self.file = archname
        return

    def update_list(self) :
        """Update self.child and self.current accroding to self.cwd."""
        self.child, self.current = self.get_current_list(self.cwd)
        return

    def get_current_list(self, cwd) :
        """Get list of child and current file. Also used for compl."""
        child = [e.replace(cwd, "", 1) for e in self.list \
                     if e.startswith(cwd)]
        current = [e for e in child if \
                       (not "/" in e and e != "") or \
                       (e.count("/") == 1 and e.endswith("/"))]
        return (child, current)

    def set_dir(self, newpath) :
        """Set self.cwd. Return new dir or None if failed."""
        d = self.get_dir(newpath)
        if d != None :
            self.cwd = d
            self.update_list()
        return d

    def get_dir(self, newpath) :
        """Calculate new path and return absolute path or None if nonexist."""
        if newpath == "/" :
            return ""
        elif newpath == "" :
            return self.cwd

        if newpath.startswith("/") : # absolute
            newd = newpath[1:]
        else :
            newd = self.cwd + newpath

        if not newd.endswith("/") :
            newd = newd + "/"
        if newd in self.list :
            return newd
        else :
            return None
