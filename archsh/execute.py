#!/usr/bin/env python3

from .tgz import TGZ

class Execute() :
    hr = None
    def __init__(self, env) :
        if env.file.endswith(".tar.gz") :
            self.hr = TGZ(env.file)    # handler
        if self.hr :
            env.set_list(self.hr.get_list())
            env.update_list()
        self.env = env
        return

    def run(self, args) :
        print(args)
        if len(args) == 0 :
            return
        elif args[0] == "cd" :
            self.run_cd(args[1:])
        elif args[0] == "ls" :
            self.run_ls(args[1:])
        return

    def run_cd(self, args) :
        if len(args) == 0 :
            self.env.set_dir("/")
        elif self.env.set_dir(args[0]) == None :
            print("cd: dir %s not found." % args[0])
        return

    def run_ls(self, args) :
        for e in self.env.current :
            print(e)
