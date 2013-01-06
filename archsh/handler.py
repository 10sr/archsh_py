#!/usr/bin/env python3

"""
Base class for archive Handler.
"""

class Handler() :
    """Base class for archive handler."""
    suffixes = []
    def __init__(self, file) :
        self.file = file
        return

    def get_list(self) :
        """Return list of files."""
        return []

    def cat_files(self, files) :
        """Return iterable of tuple (file, output).

        output is binary stream."""
        raise NotImplementedError("Method cat_files() is not implemented in " +
                                  str(self.__class__))

    def extract_files(self, files, tempdir) :
        """Return iterable of tuple (file, path).

        path is where the file was created.
        All files should be placed under tempdir."""
        raise NotImplementedError(
            "Method extract_files() is not implemented in " +
            str(self.__class__))

class FileInfo() :
    def __init__(self, name, mdate) :
        self.name = name
        self.mdate = mdate
        return
