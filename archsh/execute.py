#!/usr/bin/env python3

from .tgz import TGZ

class Execute() :
    def __init__(self, env) :
        if env.file.endswith(".tar.gz") :
            self.hr = TGZ(env.file)    # handler
        env.list = self.hr.get_list()
        return

    def run(self, env, cmds) :
        if cmds[0] == "cd" :
            self.run_cd(env, cmds)
        elif cmds[0] == "ls" :
            self.run_ls(env, cmds)
        return

    def run_cd(self, env, cmds) :
        newd = env.cwd + cmds[1]
        if not newd.endswith("/") :
            newd = newd + "/"
        if newd in env.list :
            env.cwd = newd
        return

    def run_ls(self, env, cmds) :
        child = [e.replace(env.cwd, "", 1) for e in env.list \
                     if e.startswith(env.cwd)]
        current = [e for e in child if \
                       (not "/" in e and e != "") or \
                       (e.count("/") == 1 and e.endswith("/"))]
        for e in current :
            print(e)
