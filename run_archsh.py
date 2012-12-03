#!/usr/bin/env python3

from archsh import shell
from sys import argv

if len(argv) == 2 :
    s = shell(argv[1])
    s.main()
else :
    print("invalid arg!")
