#!/usr/bin/env python3


import os
import sys


SRC = "../gna/*"
DST = "../public_repos/emox"

os.system("rsync -avzh --exclude-from .gitignore --exclude .git* %s %s" % (SRC, DST))

git_rmks = input("> commit-msg: ")

os.system("""cd %s && git add ./ && git commit -a -m "%s" && git push origin master""" % (DST, git_rmks)) 

