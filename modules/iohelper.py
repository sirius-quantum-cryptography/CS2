__author__ = "mashed-potatoes"

from os import remove, rename
from os.path import isfile


def update_file(prev, new) -> None:
    if isfile(new):
        remove(new)
    rename(prev, new)
