#!/usr/bin/env python3

"""
Base class for archive Handelr.
"""

class Handler() :
    suffixes = []
    def __init__(self, file) :
        self.file = file
        return
    def get_list(self) :
        return []
    def cat_files(self, files) :
        """Return list of tuple (file, output), where output is file object."""
        return []
    def open_files(self, files, tempdir) :
        """Return list of tuple (file, path), path is where the file created."""
        return []
