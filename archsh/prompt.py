#!/usr/bin/env python3

editor = {
    "vi" : "vi"
    }

pager = {
    "less" : "less"
    }

import fnmatch                  # maybe i can use fileter
from shlex import split as shsplit
from posixpath import split as pathsplit
from cmd import Cmd
from subprocess import call

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
    def __init__(self, env, execute) :
        self._env = env
        self._exec = execute
        # if readline :
        #     readline.set_completer_delims(" ")
        #     readline.set_completer(self._completer)
        Cmd.__init__(self)
        self.intro = "Archsh command line for archive"
        self.prompt = "%s:%s $ " % (self._env.file, self._env.cwd)
        return

    def completedefault(self, text, line, begidx, endidx) :
        # text is "" even when, for example, "cd dir\ " is written to line.
        # i ignore escaped whitespace because in that case candidates go mess.
        # for example, candidate for "/aaa/bb\ b" must be like ["b", "bb"],
        # not ["bb\ b", "bb\ bb"].
        head, tail = pathsplit(text)

        if tail == "." :
            return [text + "/", text + "./"]
        elif tail == ".." :
            return [text + "/"]

        if head == "" :
            adir = self._env.get_dir("./")
        else :
            adir = self._env.get_dir(head)

        child, current = self._env.get_current_list(adir)
        if head != "" :
            head = head + "/"
        cand = [(head + e) for e in current if e.startswith(tail)]
        return cand

    def complete_cd(self, text, line, begidx, endidx) :
        args = shsplit(line)
        if len(args) >= 3 :
            return []
        else :
            cand = self.completedefault(text, line, begidx, endidx)
            cand = [e for e in cand if e.endswith("/")]
            return cand

    def postcmd(self, stop, line) :
        self.prompt = "%s:%s $ " % (self._env.file, self._env.cwd)
        return stop

    def emptyline(self) :
        return False

    def do_exit(self, line) :
        print("Bye!.")
        return True

    def do_EOF(self, line) :
        print("")
        return self.do_exit(line)

    def do_cd(self, line) :
        """cd: Change current directory."""
        args = self._parse_line(line)
        print(args)
        self._exec.run_cd(args)
        return False

    def do_ls(self, line) :
        """ls: List current directory files."""
        args = self._parse_line(line)
        self._exec.run_ls(args)
        return False

    def do_pwd(self, line) :
        """pwd: Print current working directory."""
        print(self._env.cwd)
        return False

    def do_shell(self, line) :
        call(line, shell=True)
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
