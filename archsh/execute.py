#!/usr/bin/env python3

from .tgz import TGZ

class Execute() :
    hr = None
    def __init__(self, env) :
        if env.file.endswith(".tar.gz") :
            self.hr = TGZ(env.file)    # handler
        if self.hr :
            env.list = self.hr.get_list()
            env.update_list()
        self.env = env
        return

    def run(self, cmds) :
        print(cmds)
        if len(cmds) == 0 :
            return
        elif cmds[0] == "cd" :
            self.run_cd(cmds)
        elif cmds[0] == "ls" :
            self.run_ls(cmds)
        return

    def run_cd(self, cmds) :
        if self.env.set_dir(cmds[1]) == None :
            print("ls: dir %s not found." % cmds[1])
        return

    def run_ls(self, cmds) :
        for e in self.env.current :
            print(e)
