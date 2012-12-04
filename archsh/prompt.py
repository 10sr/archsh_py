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
    _cand = []                  # candidate for completer
    _buf = ""                   # current buffer of readline
    _arg = []                   # splitted self._buf

    def __init__(self, env) :
        self.env = env
        if readline :
            readline.set_completer_delims(" ")
            readline.set_completer(self._completer)
        return

    def input(self) :
        """Get input from user and return list of arg or None if C-c.

        cwd is pseudo current directory, list is list of all file arch contains
        """
        self.list = self.env.list

        try :
            readline.insert_text("")
            self.s = input("%s:/%s $ " % (self.env.file, self.env.cwd))
            return self._parse_input(self.s)
        except (EOFError, KeyboardInterrupt) :
            print("")
            return None


    def _completer(self, text, state) :
        def com_filter(array, text) :
            return [s for s in array if s.startswith(text)]

        if state == 0 :
            # i feel like get_line_buffer() is broken, it holds previous
            # buffer when input is empty yet.
            endidx = readline.get_endidx()
            buf = readline.get_line_buffer()[:endidx]
            if buf == "" :
                self._cand = []
            else :
                arg = shsplit(buf)
                if len(arg) == 0 :
                    curdir = self.env.cwd
                else :
                    curdir = self.env.get_dir(arg[-1]) or self.env.cwd
                child, current = self.env.get_current_list(curdir)
                self._cand = com_filter(current, text)

        try :
            return self._cand[state]
        except IndexError :
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
