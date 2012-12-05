#!/usr/bin/env python3

import fnmatch                  # maybe i can use fileter
from shlex import split as shsplit
from os.path import split as pathsplit
from cmd import Cmd

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

class ArchCmd(Cmd) :
    _cand = []                  # candidate for completer
    _buf = ""                   # current buffer of readline
    _arg = []                   # splitted self._buf

    def __init__(self, env, execute) :
        Cmd.__init__(self)
        self.intro = "Archsh command line for archive"
        self._env = env
        self._exec = execute
        # if readline :
        #     readline.set_completer_delims(" ")
        #     readline.set_completer(self._completer)
        return

    def completedefault(self, text, line, begidx, endidx) :
        # text is "" even when, for example, "cd dir\ " is written to line.
        # i ignore escaped whitespace because in that case candidates go mess.
        # for example, candidate for "/aaa/bb\ b" must be like ["b", "bb"],
        # not ["bb\ b", "bb\ bb"].
        head, tail = pathsplit(text)
        adir = self._env.get_dir(head)
        child, current = self._env.get_current_list(adir)
        if head != "" :
            head = head + "/"
        cand = [(head + e) for e in current if e.startswith(tail)]
        return cand

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

    def postcmd(self, stop, line) :
        self.prompt = "cmd %s : " % line
        return stop

    def emptyline(self) :
        return False

    def do_exit(self, line) :
        print("")
        print("Exit.")
        return True

    do_EOF = do_exit

    def do_cd(self, line) :
        """Change current directory."""
        args = self._parse_line(line)
        print(args)
        self._exec.run_cd(args)
        return False

    def do_ls(self, line) :
        """List current directory files."""
        args = self._parse_line(line)
        self._exec.run_ls(args)
        return False

    def _parse_line(self, line) :
        args = shsplit(line)
        # eargs = [args[0]]
        # for a in args[1:] :
        #     g = glob(a)
        #     if len(g) == 0 :
        #         eargs.extend([a])
        #     else :
        #         eargs.extend(g)
        return args
