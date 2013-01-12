#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT, call
from posixpath import split
from os.path import join as osjoin

from archsh.handler import Handler

class P7Z(Handler):
    suffixes = [".7z"]

    p7z_command = "7z"

    list_option = "l"
    extract_option = "x"
    cat_option = "-so"

    directory_option = "-o"

    def get_list(self):
        offset = 0
        start = False
        r = []
        p = Popen([self.p7z_command, self.list_option, self.file],
                  stdout=PIPE, stderr=STDOUT)
        for l in p.stdout:
            ul = l.decode()
            if ul.startswith("   Date"):
                offset = ul.index("Name")
            elif ul.startswith("------"):
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

    # def cat_files(self, files):
    #     for f in files:
    #         p = Popen([self.p7z_command, self.extract_option, self.file, f],
    #                   stdout=PIPE, stderr=STDOUT)
    #         yield (f,p.stdout)
    #     return

    def extract_files(self, files, tempdir):
        call([self.p7z_command, self.extract_option, \
                  self.directory_option + tempdir, self.file] + files)
        return ((f, osjoin(tempdir, f)) for f in files)
