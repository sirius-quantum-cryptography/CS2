from os import remove, rename
from os.path import isfile

def update_file(prev, new):
    if isfile(new):
        remove(new)
    rename(prev, new)
