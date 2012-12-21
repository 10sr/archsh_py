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
        """Return iterable of tuple (file, output) or None.

        output is binary stream."""
        return None

    def extract_files(self, files, tempdir) :
        """Return iterable of tuple (file, path) or None.

        path is where the file was created.
        All files should be under tempdir."""
        return None

class FileInfo() :
    def __init__(self, name, mdate) :
        self.name = name
        self.mdate = mdate
        return
