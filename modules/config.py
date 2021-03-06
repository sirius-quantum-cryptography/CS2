__author__ = "mashed-potatoes"

from os import getenv
from sys import argv

mode = getenv("cs2_mode", None) if len(argv) < 2 else argv[1]

HOME_PATH = "./data_" + mode
ALICE_KEY = HOME_PATH + "/alice.bin"
BOB_KEY = HOME_PATH + "/bob.bin"
PARITY = HOME_PATH + "/parity.bin"
BAD_BLOCKS = HOME_PATH + "/bad.bin"
TEMP = HOME_PATH + "/temp.bin"
LEN_NES = 640000
POWER = 4
ITERATIONS = 4
LEN_SHUFFLE = 4096
REMOTE_HOST = getenv(
    "cs2_remote_host", "localhost:" + str(64295 if mode == "bob" else 64296)
)
