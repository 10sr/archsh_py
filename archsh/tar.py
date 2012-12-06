#!/usr/bin/env python3

# handle tar files

from subprocess import call, check_output, Popen, PIPE, STDOUT
from os import getenv, getpid
from os.path import join as osjoin

class ArchHandler() :
    suffixes = []
    def __init__(self, file, tmpdir) :
        self.file = file
        self.tmpdir = tmpdir
        return
    def get_list(self) :
        return []
    def cat_files(self, *files) :
        """Return list of tuple (file, output), where output is file object."""
        return []
    def open_files(self, *files) :
        """Return list of tuple (file, path), path is where the file created."""
        return []

class TAR(ArchHandler) :
    suffixes = [".tar"]
    list_command = ["tar", "-tf"]
    cat_command = ["tar", "-xOf"]
    extract_command = ["tar", "-xf"]

    def get_list(self) :
        lst = check_output(self.list_command + [self.file]).decode().split("\n")
        self.list = [e for e in lst if e != ""]
        return self.list

    def cat_files(self, *files) :
        r = []
        for f in files :
            p = Popen(self.cat_command + [self.file, f],
                      stdout=PIPE, stderr=STDOUT)
            r.append((f, p.stdout))
        return r

    def open_files(self, *files) :
        lfiles = list(files)
        call(self.extract_command + [self.file, "-C", self.tmpdir] + lfiles)
        return [(f, osjoin(self.tmpdir, f)) for f in files]

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
