__author__ = "mashed-potatoes"

from threading import Thread
from os import _exit
from modules.hamming import *
from modules.config import *
from modules.iohelper import update_file
from modules.sender import RemoteHost
from modules.http_server import NetIO
from modules.logger import Logger
from modules.qber import calc_ber
from pymitter import EventEmitter

ee = EventEmitter()
l = Logger()
server = NetIO(64296)
rh = RemoteHost(REMOTE_HOST, l)
iteration = 0


@ee.on("parity generated")
def on_patrity_generated(sid):
    l.ok()
    rh.emit("send parity")


@ee.on("parity sent")
def on_parity_received(sid):
    global LEN_NES
    l.ok()
    l.proc("Generating bad blocks")
    hamming_correct(
        BOB_KEY, PARITY, TEMP, BAD_BLOCKS, POWER, len_nes=LEN_NES // 11, drop_bad=True
    )
    l.ok()
    update_file(TEMP, BOB_KEY)
    l.proc("Shuffling key")
    shuffle(BOB_KEY, TEMP, LEN_SHUFFLE, 0)
    update_file(TEMP, BOB_KEY)
    l.ok()
    l.proc("Sending badblocks")
    rh.send_file(BAD_BLOCKS)
    l.ok()
    LEN_NES = 0
    l.proc("Wiping badblocks")
    rh.emit("wipe badblocks", LEN_NES)


@ee.on("blocks wiped")
def on_blocks_wiped(sid):
    l.ok()
    rh.emit("shuffle key")


@ee.on("iteration ended")
def on_next_iteration(sid):
    global iteration
    if iteration == ITERATIONS:
        l.info("Task finished!")
        calc_ber(l)
        l.proc("Terminating Alice")
        rh.emit("exit")
        l.ok()
        _exit(0)
    l.info(f"*** THE ITERATION {iteration + 1} of {ITERATIONS} ***")
    calc_ber(l)
    iteration += 1
    rh.emit("generate parity")


@ee.on("message")
def message(args):
    global iteration
    l.info(f"New message from remote host: {args}")
    l.proc("Generating parity")
    rh.emit("generate parity")
    iteration += 1


def recover_keys():
    import subprocess

    subprocess.call(["bash", "recover_keys.sh"])
    l.info("Keys recovered")


def run():
    global server
    l.info("Running Bob...")
    # Debug only
    recover_keys()
    server.set_emitter(ee)
    Thread(target=server.start).start()
