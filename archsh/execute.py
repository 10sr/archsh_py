#!/usr/bin/env python3

handlers = []
from .tar import TAR, TGZ, TBZ, TXZ
handlers.extend([TAR, TGZ, TBZ, TXZ])

from .zip import ZIP
handlers.append(ZIP)

from posixpath import normpath, join
from subprocess import call
from os.path import join as osjoin, basename as osbasename, dirname
from os import rename, mkdir, makedirs, access, F_OK
from tempfile import mkdtemp, TemporaryDirectory as TempDir

try :                           # this module is available only after 3.3
    from shutil import get_terminal_size
except ImportError :
    from os import getenv
    def get_terminal_size() :
        return (getenv("COLUMNS") or "80", getenv("LINES") or "24")

class Execute() :
    handler = None
    outdir = None

    def __init__(self, env) :
        # TemporaryDirectory() also can be used
        for h in handlers :
            for s in h.suffixes :
                if env.find_suffix(s) :
                    self.handler = h(env.file)
                    break
            if self.handler :
                break

        if self.handler :
            env.set_list(self.handler.get_list())
        self.env = env
        return

    def conv_path(self, args) :
        """Convert pathes so that they can be passed to handler."""
        r = [normpath(join(self.env.pwd(), f)).lstrip("/") for f in args]
        return r

    def run_cd(self, args) :
        if len(args) == 0 :
            self.env.set_dir()
        elif self.env.set_dir(args[0]) == None :
            print("cd: dir {} not found.".format(args[0]))
        return

    def run_ls(self, args) :
        flist = self.env.current
        num = len(flist)

        if num == 0 :
            return

        size = get_terminal_size()
        col = int(size[0]) - 1
        m = max([len(e) for e in flist]) + 1
        items = [(f + " " * m)[:m] for f in flist]
        qt, rem = divmod(num * m, col)
        if rem == 0 :
            rows = qt
        else :
            rows = qt + 1

        lines = [""] * rows     # what is the best way to make list?
        i = 0
        for f in items :
            lines[i] += f
            if i == rows - 1 :
                i = 0
            else :
                i += 1

        for l in lines :
            print(l)

        return

    def run_get(self, files, path=False, force=False) :
        with TempDir(prefix="archsh-") as tempdir :
            afiles = self.conv_path(files)
            if path :
                if not self.outdir :
                    self.outdir = mkdtemp(prefix=self.env.basename + "-",
                                          dir=".")
                for e in self.handler.open_files(afiles, tempdir) :
                    dst = osjoin(self.outdir, e[0])
                    try :
                        makedirs(dirname(dst))
                    except OSError :
                        pass
                    rename(e[1], dst)
                    print("'{}' -> '{}'".format(e[0], dst))
            else :
                for e in self.handler.open_files(afiles, tempdir) :
                    dst = osjoin(".", osbasename(e[1]))
                    if access(dst, F_OK) and force == False :
                        print("'{}' already exist. Consider using getd.".\
                                  format(dst))
                    else :
                        rename(e[1], dst)
                        print("'{}' -> '{}'".format(e[0], dst))
        return

    def run_pager(self, files, program) :
        # should use temp file and open at once?
        afiles = self.conv_path(files)
        for e in self.handler.cat_files(afiles) :
            if program == "cat" :
                for l in e[1] :
                    print(l.decode(), end="")
            else :
                call([program], stdin=e[1])
            e[1].close()
        return

    def run_editor(self, files, program) :
        return
