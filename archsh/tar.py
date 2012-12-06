#!/usr/bin/env python3

# handle gzip (.tar.gz) file

from subprocess import check_output, Popen, PIPE, STDOUT

class TAR() :
    suffixes = [".tar"]
    list_command = ["tar", "-tf"]
    cat_command = ["tar", "-xOf"]

    def __init__(self, file) :
        self.file = file
        return

    def get_list(self) :
        lst = check_output(self.list_command + [self.file]).decode().split("\n")
        self.list = [e for e in lst if e != ""]
        return self.list

    def cat_files(self, *files) :
        """Return list of tuple (file, output), where output is file object."""
        r = []
        for f in files :
            p = Popen(self.cat_command + [self.file] + [f],
                      stdout=PIPE, stderr=STDOUT)
            r.append((f, p.stdout))
        return r

    def open_files(self, *files) :
        return None

class TGZ(TAR) :
    suffixes = [".tar.gz", ".tgz"]
    list_command = ["tar", "-tzf"]
    cat_command = ["tar", "-xzOf"]

class TBZ(TAR) :
    suffixes = [".tar.bz2", ".tbz"]
    list_command = ["tar", "-tjf"]
    cat_command = ["tar", "-xjOf"]

class TXZ(TAR) :
    suffixes = [".tar.xz", ".txz"]
    list_command = ["tar", "-tJf"]
    cat_command = ["tar", "-xJOf"]
