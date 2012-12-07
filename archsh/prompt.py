#!/usr/bin/env python3

import fnmatch                  # maybe i can use filter
from shlex import split as shsplit
from posixpath import split as pathsplit
from cmd import Cmd
from subprocess import call
from os import getenv

try:
    import readline
except ImportError:
    print("Module readline not available.")
    readline = None
else:
    # dirty fix
    # When using osx, delimitter "/" not works and use " " splitted string
    # for completion. On Linux "/" of course can be used for delim, but it
    # breaks the function of ArchCmd._completer() so disable using "/" as a
    # delimitter.
    readline.set_completer_delims(" ")
    if "libedit" in readline.__doc__ :
        readline.parse_and_bind("bind ^I rl_complete")
    else :
        readline.parse_and_bind("tab: complete")

class ArchCmd(Cmd) :
    def __init__(self, env=None, execute=None) :
        self._env = env
        self._exec = execute

        self.intro = "Archsh command line for archive"
        try :
            self.prompt = "{}:{} $ ".format(self._env.file, self._env.cwd)
        except AttributeError :
            pass

        setattr(self, "do_more", self.do_less)

        Cmd.__init__(self)
        return

    def get_names(self) :
        # Originaly this met is defined as 'return dir(self.__class__)',
        # I cannot figure out why it is such.
        return dir(self)

    def completedefault(self, text, line, begidx, endidx) :
        cand = self._complete(text)
        if len(cand) == 1 and not cand[0].endswith("/") :
            return [cand[0] + " "]
        else :
            return cand

    def complete_cd(self, text, line, begidx, endidx) :
        args = shsplit(line)
        if len(args) >= 3 :
            return []
        else :
            cand = self._complete(text)
            cand = [e for e in cand if e.endswith("/")]
            return cand

    def _complete(self, text) :
        # TEXT is "" even when, for example, "cd dir\ " is written to line.
        # I ignore escaped whitespace because in that case candidates go mess.
        # For example, candidate for "/aaa/bb\ b" must be like ["b", "bb"],
        # not ["bb\ b", "bb\ bb"].
        head, tail = pathsplit(text)

        if head == "" :
            adir = self._env.get_dir("./")
        else :
            adir = self._env.get_dir(head)

        child, current = self._env.get_current_list(adir)
        if head != "" :
            head = head + "/"
        cand = [(head + e) for e in current if e.startswith(tail)]

        if tail == "." :
            cand.insert(0, "../")
            cand.insert(0, "./")
        elif tail == ".." :
            cand.insert(0, "../")

        return cand

    def postcmd(self, stop, line) :
        self.prompt = "{}:{} $ ".format(self._env.file, self._env.cwd)
        return stop

    def emptyline(self) :
        return False

    def default(self, line) :
        if line.startswith("_debug") :
            print(line)
            print("file:{},suffix:{},basename:{}".format(
                    self._env.file, self._env.suffix, self._env.basename))
            print("tmpdir:{}".format(self._exec.tmpdir))
            return False
        else :
            return Cmd.default(self, line)

    def do_exit(self, line) :
        """Exit archsh shell."""
        print("Bye!")
        return True

    do_EOF = do_exit
    # def do_EOF(self, line) :
    #     """Exit archsh shell."""
    #     print("")
    #     return self.do_exit(line)

    def do_get(self, line) :
        """Extract file from archive."""
        args = self._parse_line(line)
        self._exec.run_get(args, False)
        return False

    def do_getd(self, line) :
        """Extract file from archive with path."""
        args = self._parse_line(line)
        self._exec.run_get(args, True)
        return False

    def do_put(self, line) :
        return False

    def call_pager(self, line) :
        print(globals()["dict"])

    def do_less(self, line) :
        """less: View file contents with less."""
        args = self._parse_line(line)
        self._exec.run_pager(args, "less")
        return False

    def do_cat(self, line) :
        """cat: cat file contents."""
        args = self._parse_line(line)
        self._exec.run_pager(args, "cat")
        return False

    def do_vi(self, line) :
        """vi: Edit file."""
        args = self._parse_line(line)
        self._exec.run_editor(args, "vi")
        return False

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
        """shell: Run external shell command."""
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
