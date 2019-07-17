from os import getenv
from sys import argv

mode = getenv("cs2_mode", None) if len(argv) < 2 else argv[1]
if not mode:
    print("Mode not present")
    exit()

module = __import__(mode)
module.run()
