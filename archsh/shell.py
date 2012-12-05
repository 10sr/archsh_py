#!/usr/bin/env python3

from .prompt import ArchCmd
from .execute import Execute

from posixpath import normpath, join

class Shell() :
    def __init__(self, archname) :
        self.e = Environ(archname)
        self.x = Execute(self.e)
        self.c = ArchCmd(self.e, self.x)
        # for e in self.e.list :
        #     print(e)
        return

    def main(self) :
        if self.x.handler :
            self.c.cmdloop()
        else :
            print("No handler found for %s." % self.e.file)
        return

class Environ() :
    file = ""                   # filename of archive
    cwd = "/"                    # cwd starts and ends with "/"
    list = []                   # all file list with leading "/", ro
    child = []                  # list of file under current dir, relative
    current = []                # file list current dir contains, relative
    def __init__(self, archname) :
        self.file = archname
        return

    def set_list(self, list) :
        """Set self.list. This met is meant to be called only once."""
        self.list = ["/" + e for e in list]
        self.list.append("/")
        return self.list

    def update_list(self) :
        """Update self.child and self.current accroding to self.cwd ."""
        self.child, self.current = self.get_current_list(self.cwd)
        return

    def get_current_list(self, cwd) :
        """Get list of child and current file. Also used for compl.

        CWD must be absolute path.
        This method does not overwrite any member."""
        child = [e.replace(cwd, "", 1) for e in self.list \
                     if e.startswith(cwd)]
        current = [e for e in child if \
                       # file
                       (not "/" in e and e != "") or \
                       # directory
                       (e.count("/") == 1 and e.endswith("/"))]
        return (child, current)

    def set_dir(self, newpath=None) :
        """Set self.cwd. Return new dir or None if failed."""
        d = self.get_dir(newpath)
        if d != None :
            self.cwd = d
            self.update_list()
        return d

    def get_dir(self, newpath=None) :
        """Calculate new path and return absolute path or None if nonexist.

        This method do not overwrite any member.
        NEWPATH can be absolute or relative.
        If NEWPATH is empty string or None, it returns root directory."""
        if newpath == "" or newpath == None :
            return "/"

        # if newpath.startswith("/") : # absolute
        #     newd = newpath
        # else :
        #     newd = self.cwd + newpath
        newd = join(self.cwd, newpath)
        newd = normpath(newd)   # remove "." or ".."
        if not newd.endswith("/") :
            # usually normpath strips last "/"
            newd = newd + "/"

        if newd in self.list :
            return newd
        else :
            return None
