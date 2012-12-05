#!/usr/bin/env python3

# handle gzip (.tar.gz) file

from subprocess import check_output as output

class TGZ() :
    def __init__(self, file) :
        self.file = file
        return

    def get_list(self) :
        lst = output(["tar", "-tzf", self.file]).decode().split("\n")
        self.list = [e for e in lst if e != ""]
        return self.list

    def cat_file(self, *files) :
        return None

    def edit_file(self, *files) :
        return None
