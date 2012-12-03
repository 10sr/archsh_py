#!/usr/bin/env python3

import fnmatch                  # maybe i can use fileter
from shlex import split as shsplit

try:
    import readline
except ImportError:
    print("Module readline not available.")
    readline = None
else:
    if "libedit" in readline.__doc__ :
        readline.parse_and_bind("bind ^I rl_complete")
    else :
        readline.parse_and_bind("tab: complete")

class Prompt() :
    def __init__(self, env) :
        if readline :
            readline.set_completer(self._completer)
        return

    def input(self, env) :
        """Get input from user and return list of arg or None if C-c.

        cwd is pseudo current directory, list is list of all file arch contains
        """
        self.list = env.list

        try :
            self.s = input("%s:%s $ " % (env.file, env.cwd))
            return self._parse_input(self.s)
        except (EOFError, KeyboardInterrupt) :
            print("")
            return None


    def _completer(self, text, state) :
        def com_filter(array, text) :
            return [s for s in array if s.startswith(text)]

        b = readline.get_line_buffer()
        for c in self.cmds :
            if b.startswith(c + " ") :
                if state == 0 :
                    self._c = com_filter(os.listdir(text or "."), text)
                if state < len(self._c) :
                    return self._c[state]
                else :
                    return None

        if state == 0 :
            self._c = com_filter(self.cmds, text)
        if state < len(self._c) :
            return self._c[state] + " "
        else :
            return None

    def _parse_input(self, input) :
        if input == "" :
            self.r = []
            return self.r

        args = shsplit(input)
        # eargs = [args[0]]
        # for a in args[1:] :
        #     g = glob(a)
        #     if len(g) == 0 :
        #         eargs.extend([a])
        #     else :
        #         eargs.extend(g)
        self.r = args
        return self.r
