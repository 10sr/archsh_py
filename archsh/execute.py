#!/usr/bin/env python3

from .tgz import TGZ

class Execute() :
    def __init__(self, env) :
        if env.file.endswith(".tar.gz") :
            self.hr = TGZ(env.file)    # handler
        env.list = self.hr.get_list()
        return

    def run(self, env, cmds) :
        pass
