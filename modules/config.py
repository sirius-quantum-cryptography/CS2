from os import getenv
from sys import argv

mode = getenv("cs2_mode", None) if len(argv) < 2 else argv[1]

HOME_PATH = "./data_" + mode
ALICE_KEY = HOME_PATH + "/alice.bin"
BOB_KEY = HOME_PATH + "/bob.bin"
PARITY = HOME_PATH + "/parity.bin"
BAD_BLOCKS = HOME_PATH + "/bad.bin"
TEMP = HOME_PATH + "/temp.bin"
LEN_NES = 64000
POWER = 4
ITERATIONS = 3
LEN_SHUFFLE = 1024
REMOTE_HOST = getenv(
    "cs2_remote_host", "localhost:" + str(64295 if mode == "bob" else 64296)
)
