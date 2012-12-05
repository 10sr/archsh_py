#!/usr/bin/env python3

from posixpath import normpath, join
from subprocess import call

from .tgz import TGZ

class Execute() :
    handler = None
    def __init__(self, env) :
        if env.file.endswith(".tar.gz") :
            self.handler = TGZ(env.file)
        if self.handler :
            env.set_list(self.handler.get_list())
            env.update_list()
        self.env = env
        return

    def conv_path(self, args) :
        """Convert pathes so that they can be passed to handler."""
        r = [normpath(join(self.env.cwd, f)).lstrip("/") for f in args]
        return r

    def run_cd(self, args) :
        if len(args) == 0 :
            self.env.set_dir()
        elif self.env.set_dir(args[0]) == None :
            print("cd: dir %s not found." % args[0])
        return

    def run_ls(self, args) :
        for e in self.env.current :
            print(e)

    def run_pager(self, files, program) :
        # should use temp file and open at once?
        afiles = self.conv_path(files)
        for e in self.handler.cat_files(*afiles) :
            if program == "cat" :
                print(e[1].read())
            else :
                call([program], stdin=e[1])
            e[1].close()
        return

    def run_editor(self, files, program) :
        return
