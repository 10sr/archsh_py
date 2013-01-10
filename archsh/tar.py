#!/usr/bin/env python3

# handle tar files

from subprocess import call, check_output, Popen, PIPE, STDOUT
from os.path import join as osjoin

from .handler import Handler

class TAR(Handler):
    suffixes = [".tar"]

    tar_command = "tar"
    file_option = "-f"
    directory_option = "-C"
    cat_option = "-O"

    list_option = "-t"
    extract_option = "-x"

    def get_list(self):
        lst = check_output([self.tar_command, self.list_option,
                            self.file_option, self.file]).decode().split("\n")
        self.list = [e for e in lst if e != ""]
        return self.list

    def cat_files(self, files):
        # this is not good. extract all files at once.
        for f in files:
            p = Popen([self.tar_command, self.extract_option, self.cat_option,
                       self.file_option, self.file, f],
                      stdout=PIPE, stderr=STDOUT)
            yield (f, p.stdout)

    def extract_files(self, files, tempdir):
        call([self.tar_command, self.extract_option, self.file_option,
              self.file, self.directory_option, tempdir] + files)
        return ((f, osjoin(tempdir, f)) for f in files)

class TGZ(TAR):
    suffixes = [".tar.gz", ".tgz"]
    list_option = "-tz"
    extract_option = "-xz"

class TBZ(TAR):
    suffixes = [".tar.bz2", ".tbz"]
    list_option = "-tj"
    extract_option = "-xj"

class TXZ(TAR):
    suffixes = [".tar.xz", ".txz"]
    list_option = "-tJ"
    extract_option = "-xJ"
