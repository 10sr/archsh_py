#!/usr/bin/env python3

from posixpath import normpath, join, split

class Environ():
    file = ""                   # Filename of archive.
    type = None                 # File type.
    suffix = ""                 # Suffix.
    basename = ""               # Filename without suffix.
    cwd = "/"                   # Cwd starts and ends with "/".
    list = []                   # All file list with leading "/", ro.
    child = []                  # List of file under current dir, relative.
    current = []                # File list current dir contains, relative.

    def __init__(self, archname, filetype=None):
        self.file = archname
        if filetype:
            self.type = filetype
        return

    def find_suffix(self, suffix):
        """Test if suffix is ext of self.filename. If so, set self.suffix,
        self.basename and return True, otherwise return False."""
        if self.file.endswith(suffix):
            self.suffix = suffix
            nslen = len(suffix) * (-1)
            self.basename = self.file[:nslen]
            return True
        else:
            return False

    def set_list(self, lst):
        """Set self.list. This met is meant to be called only once.

        LST is list of files in archive. For example, if dir tree is like:

        dir/
        |--file1
        `--file2

        LST should be like any of:

            lst = ['dir', 'dir/file1', 'dir/file2']
        or
            lst = ['dir/', 'dir/file1', 'dir/file2']
        or
            lst = ['dir/file1', 'dir/file2']
        """
        self.list = ["/" + e for e in lst]

        # remove dirs without trailing "/"
        for f in list(self.list):
            if any(ff.startswith(f + "/") for ff in self.list):
                self.list.remove(f)

        # add dir entries
        for f in list(self.list):
            elems = f.lstrip("/").split("/")[:-1] # last one is filename
            d = "/"
            for e in elems:
                d = d + e + "/"
                if not d in self.list:
                    self.list.append(d)
        self.list.append("/")
        self.update_list()
        return self.list

    def update_list(self):
        """Update self.child and self.current accroding to self.cwd ."""
        self.child, self.current = self.get_current_list(self.cwd)
        return

    def get_current_list(self, cwd=None):
        """Get list of child and current file relative path. Also used for
        compl.

        CWD must be absolute path.
        This method does not overwrite any member."""
        if cwd == None:
            cwd = self.cwd
        else:
            cwd = self.get_dir(cwd)

        children = [e.replace(cwd, "", 1) for e in self.list \
                        if e.startswith(cwd)]
        current = [e for e in children if \
                       # file
                   (not "/" in e and e != "") or \
                       # directory
                   (e.count("/") == 1 and e.endswith("/"))]
        return (children, current)

    def pwd(self):
        """Print current working directory without trailing `/'."""
        if self.cwd == "/":
            return "/"
        else:
            return self.cwd.rstrip("/")

    def set_dir(self, newpath=None):
        """Set self.cwd. Return new dir or None if failed."""
        d = self.get_dir(newpath)
        if d != None:
            self.cwd = d
            self.update_list()
        return d

    def get_dir(self, newpath=None):
        """Calculate new path and return absolute path or None if nonexist.

        Return value is like /dir/.
        This method do not overwrite any member.
        NEWPATH can be absolute or relative.
        If NEWPATH is empty string or None, it returns root directory."""
        if newpath == "" or newpath == None:
            return "/"

        # if newpath.startswith("/") : # absolute
        #     newd = newpath
        # else:
        #     newd = self.cwd + newpath
        newd = join(self.cwd, newpath)
        newd = normpath(newd)   # remove "." or ".."
        if not newd.endswith("/"):
            # usually normpath strips last "/"
            newd = newd + "/"

        if newd in self.list:
            return newd
        else:
            return None
