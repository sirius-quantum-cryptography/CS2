from threading import Thread
from os import _exit
from modules.hamming import *
from modules.config import *
from modules.iohelper import update_file
from modules.sender import RemoteHost
from modules.http_server import NetIO
from modules.logger import Logger
from pymitter import EventEmitter

ee = EventEmitter()
server = NetIO(64296)
rh = RemoteHost(REMOTE_HOST)
l = Logger()
iteration = 0

@ee.on("parity generated")
def on_patrity_generated(sid):
    print("Alice generated parity")
    rh.emit("send parity")


@ee.on("parity sent")
def on_parity_received(sid):
    global LEN_NES
    print("Parity received!")
    print("Generating bad blocks... ", end="")
    hamming_correct(
        BOB_KEY,
        PARITY,
        TEMP,
        BAD_BLOCKS,
        POWER,
        len_nes=LEN_NES // 11,
        drop_bad=True,
    )
    update_file(TEMP, BOB_KEY)
    print("OK\nShuffling key... ", end="")
    shuffle(BOB_KEY, TEMP, LEN_SHUFFLE, 0)
    update_file(TEMP, BOB_KEY)
    print("OK\nSending badblocks... ", end="")
    rh.send_file(BAD_BLOCKS)
    print("OK")
    LEN_NES = 0
    rh.emit("wipe badblocks", LEN_NES)


@ee.on("blocks wiped")
def on_blocks_wiped(sid):
    print("Blocks wiped")
    rh.emit("shuffle key")


@ee.on("iteration ended")
def on_next_iteration(sid):
    global iteration
    if iteration == ITERATIONS:
        print("Task finished!")
        print("Terminating Alice... ", end='')
        rh.emit('exit')
        print('OK')
        _exit(0)
    print(f"*** THE ITERATION {iteration + 1} of {ITERATIONS} ***")
    iteration += 1
    rh.emit("generate parity")


@ee.on("message")
def message(args):
    global iteration
    print("New message from remote host:", args)
    print("Alice is generating parity...")
    rh.emit("generate parity")
    iteration += 1


def recover_keys():
    import subprocess
    subprocess.call(['bash', 'recover_keys.sh'])


def run():
    global server
    print("Running Bob...")
    # Debug only
    recover_keys()
    server.set_emitter(ee)
    Thread(target=server.start).start()
