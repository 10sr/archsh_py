#!/usr/bin/env python3

handlers = []
from .tar import TAR, TGZ, TBZ, TXZ
handlers.extend([TAR, TGZ, TBZ, TXZ])

from .zip import ZIP
handlers.append(ZIP)

from .p7z import P7Z
handlers.append(P7Z)

from posixpath import normpath, join
from subprocess import call
from os.path import join as osjoin, basename as osbasename, dirname
from os import mkdir, makedirs, access, F_OK
from shutil import move
from tempfile import mkdtemp, TemporaryDirectory as TempDir
from random import random

try :                           # this function is available only after 3.3
    from shutil import get_terminal_size
except ImportError :
    from os import getenv
    def get_terminal_size() :
        return (getenv("COLUMNS") or "80", getenv("LINES") or "24")

def mk_temp_dir(dir, prefix) :
    def randstr() :
        return hex(hash(random()))[2:7]

    base = osjoin(dir, prefix)
    while True :
        try :
            newdir = base + randstr()
            mkdir(newdir)
            return newdir
        except OSError :
            pass

class Execute() :
    handler = None
    outdir = None

    def __init__(self, env) :
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

    def run_ls(self, args, all=True) :
        flist = sorted(self.env.current) # copied list
        if not all :
            flist = [f for f in flist if not f.startswith(".")]
        num = len(flist)

        if num == 0 :
            return

        size = get_terminal_size()
        col = int(size[0]) - 1
        m = max([len(e) for e in flist]) + 1
        items = [f.ljust(m) for f in flist]
        prow, rem = divmod(col, m)
        rows = num // prow
        if rem != 0 or rows == 0 :
            rows += 1

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

        def make_file(path, dst, use_stream, arg, force=False) :
            """Create file."""
            try :
                makedirs(dirname(dst))
            except OSError :
                pass

            if access(dst, F_OK) and force == False :
                print("'{}' alread exists.".format(dst))
            else :
                if use_stream :
                    fo = open(dst, mode="wb")
                    fo.write(arg.read())
                    fo.close()
                else :
                    move(arg, dst)
                print("'{}' -> '{}'".format(path, dst))

            if use_stream :
                arg.close()

            return

        def make_out_path(f, d=None) :
            if d :
                return osjoin(d, f)
            else :
                return osjoin(".", osbasename(f))

        afiles = self.conv_path(files)
        with TempDir(prefix="archsh-") as tempdir :
            r = self.handler.extract_files(afiles, tempdir)
            if r :
                use_stream = False
            else :
                r = self.handler.cat_files(afiles)
                if r :
                    use_stream = True
                else :
                    print("That operation is not supported for this archive.")
                    return

            if path :
                if not self.outdir :
                    self.outdir = mk_temp_dir(prefix=self.env.basename + "-",
                                                dir=".")
                outdir = self.outdir
            else :
                outdir = None

            for f, out in r :
                dst = make_out_path(f, outdir)
                make_file(f, dst, use_stream, out, force)

        return

    def run_pager_from_stream(self, program ,l) :
        for f, out in l :
            if program == "cat" :
                for l in out :
                    print(l.decode(), end="")
            else :
                call([program], stdin=out)
            out.close()
        return

    def run_pager_from_file(self, program, l) :
        if program == "cat" :
            for f, out in l :
                with open(out, "r") as fo :
                    for l in fo :
                        print(l, end="")
        else :
            call([program] + [i[1] for i in l])
        return

    def run_pager(self, files, program) :
        # should use temp file and open at once?
        afiles = self.conv_path(files)
        r = self.handler.cat_files(afiles)
        if r :
            self.run_pager_from_stream(program, r)
        else :
            with TempDir(prefix="archsh-") as tempdir :
                r = self.handler.extract_files(afiles, tempdir)
                if r :
                    self.run_pager_from_file(program, r)
                else :
                    print("That operation is not supported for this archive.")
        return

    def run_editor(self, files, program) :
        return
