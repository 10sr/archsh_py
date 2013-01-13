#!/usr/bin/env python3

"""Archive Handler.

Writing handlers
================

1. Write class that inherits `Handler' and implement get_list and (cat_files
   and/or extract_files).
2. Add the class to list execute.handlers .
"""

class Handler():
    """Base class for archive handler.

    Attributes:
        file: Filename of archive.
        suffixes: List of suffixes representing file types this handler
            supports.
    """
    suffixes = []
    def __init__(self, file):
        self.file = file
        return

    def get_list(self):
        """Return list of files.

        Returns:
            List of files in archive. For example, if archive contains files
            like:

                dir/
                |--file1
                `--file2

            return of this method should be like any of:

                ['dir', 'dir/file1', 'dir/file2']
                ['dir/', 'dir/file1', 'dir/file2']
                ['dir/file1', 'dir/file2']
        """
        raise NotImplementedError(
            "Cannot get file list of {}".format(self.file))

    def cat_files(self, files):
        """Get file contents without extracting it into files.

        Get file object for given files. Commands `cat' and `less' first try to
        use this method. If this method is not implemented, next try
        extract_files().

        Args:
            files: List of file pathes to get, like ["file1", "dir1/file2"].

        Returns:
            Iterable of tupple like (file, output), where `file' is same as
            element of arg `files' and `output' is file object that contains
            file content as bytes.
        """
        raise NotImplementedError(
            "Method cat_files() is not implemented in " + str(self.__class__))

    def extract_files(self, files, tempdir):
        """Extract files.

        Extract files and return the pathes. Many commands first try to use
        this method. If this method is not implemented, next try cat_files().

        Args:
            files: List of file pathes to extract, like ["file1", "dir1/file2"].
            tempdir: Path of temporary directory prepared for current call. All
                extracted files should be put into this directory.

        Returns:
            Iterable of tuple like (file, path), where `file' is same as
            element of arg `files' and `path' is path to extracted file.
        """
        raise NotImplementedError(
            "Method extract_files() is not implemented in " +
            str(self.__class__))

# class FileInfo():
#     def __init__(self, name, mdate):
#         self.name = name
#         self.mdate = mdate
#         return
