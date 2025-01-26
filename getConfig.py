import os
import sys

def getCurrentDirectory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))
