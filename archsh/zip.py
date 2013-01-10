#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT, call
from posixpath import split
from os.path import join as osjoin
from .handler import Handler

class ZIP(Handler):
    suffixes = [".zip", ".xpi"]

    unzip_command = "unzip"

    list_option = "-l"
    cat_option = "-p"

    directory_option = "-d"

    def get_list(self):
        offset = 0
        start = False
        r = []
        p = Popen([self.unzip_command, self.list_option, self.file],
                  stdout=PIPE, stderr=STDOUT)
        for l in p.stdout:
            ul = l.decode()
            if ul.startswith("  Length"):
                offset = ul.index("Name")
            elif ul.startswith(" --------") or ul.startswith("---------"):
                if not start:
                    start = True
                else:
                    break
            elif not start:
                pass
            else:
                r.append(ul[offset:].rstrip("\n"))

        p.stdout.close()
        return r

    def cat_files(self, files):
        for f in files:
            p = Popen([self.unzip_command, self.cat_option, self.file, f],
                      stdout=PIPE, stderr=STDOUT)
            yield (f,p.stdout)

    def extract_files(self, files, tempdir):
        call([self.unzip_command, self.file] + files + \
                 [self.directory_option, tempdir])
        return ((f, osjoin(tempdir, f)) for f in files)
