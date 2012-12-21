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
        return []
    def cat_files(self, files) :
        """Return list of tuple (file, output),

        output is file object."""
        return []
    def open_files(self, files, tempdir) :
        """Currently this met is not needed for get file."""
        """Return list of tuple (file, path).

        path is where the file was created."""
        return []

class FileInfo() :
    def __init__(self, name, mdate) :
        self.name = name
        self.mdate = mdate
        return
