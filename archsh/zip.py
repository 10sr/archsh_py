#!/usr/bin/env python3

from subprocess import Popen, PIPE, STDOUT
from .handler import Handler

class ZIP(Handler) :
    suffixes = [".zip"]

    unzip_command = "unzip"

    list_option = "-l"
    cat_option = "-p"

    def get_list(self) :
        offset = 0
        start = False
        r = []
        p = Popen([self.unzip_command, self.list_option, self.file],
                  stdout=PIPE, stderr=STDOUT)
        for l in p.stdout :
            ul = l.decode()
            if ul.startswith("  Length") :
                offset = ul.index("Name")
            elif ul.startswith(" --------") :
                if not start :
                    start = True
                else :
                    break
            elif not start :
                pass
            else :
                r.append(ul[offset:].rstrip("\n"))

        p.stdout.close()
        return r

    def cat_files(self, files) :
        for f in files :
            p = Popen([self.unzip_command, self.cat_option, self.file, f],
                      stdout=PIPE, stderr=STDOUT)
            yield (f,p.stdout)
        return
