#!/usr/bin/env python3

# handle gzip (.tar.gz) file

from subprocess import check_output, Popen, PIPE, STDOUT

class TGZ() :
    def __init__(self, file) :
        self.file = file
        return

    def get_list(self) :
        lst = check_output(["tar", "-tzf", self.file]).decode().split("\n")
        self.list = [e for e in lst if e != ""]
        return self.list

    def cat_files(self, *files) :
        """Return list of tuple (file, output), where output is file object."""
        r = []
        for f in files :
            p = Popen(["tar", "-xf", self.file, "-O", f],
                      stdout=PIPE, stderr=STDOUT)
            r.append((f, p.stdout))
        return r

    def edit_files(self, *files) :
        return None
