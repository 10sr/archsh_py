#!/usr/bin/env python3

from distutils.core import setup

import archsh

setup(name = "archsh",
      version = archsh.__version__,
      description = "Shell for Archive",
      long_description = archsh.__doc__,
      author = "10sr",
      author_email = "sr10@sourceforge.org",
      url = "https://github.com/10sr/archsh_py",
      download_url = "https://github.com/10sr/archsh_py/archive/master.zip",
      packages = ["archsh", "archsh/handler"],
      scripts = ["bin/archsh"],
      keywords = "archive utility",
      classifiers=['License :: Public Domain']
      )
