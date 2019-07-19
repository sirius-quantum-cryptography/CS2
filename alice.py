__author__ = "mashed-potatoes"

from threading import Thread
from os import _exit
from modules.config import *
from modules.hamming import *
from modules.sender import RemoteHost
from modules.iohelper import update_file
from modules.http_server import NetIO
from modules.logger import Logger
from pymitter import EventEmitter

ee = EventEmitter()
l = Logger()
server = NetIO(64295)
rh = RemoteHost(REMOTE_HOST, l)


@ee.on("generate parity")
def on_generate_parity(data):
    l.proc("Generating parity")
    hamming_parity(ALICE_KEY, PARITY, POWER, LEN_NES)
    rh.emit("parity generated")
    l.ok()


@ee.on("send parity")
def on_parity_requested(data):
    l.proc("Sending parity")
    rh.send_file(PARITY)
    l.ok()
    l.proc("Waiting for a Bob")
    rh.emit("parity sent")


@ee.on("wipe badblocks")
def on_wipe_badblocks(data):
    global LEN_NES
    l.ok()
    l.proc("Wiping badblocks")
    hamming_wipe(ALICE_KEY, TEMP, BAD_BLOCKS, POWER, len_nes=LEN_NES // 11)
    update_file(TEMP, ALICE_KEY)
    l.ok()
    rh.emit("blocks wiped")
    LEN_NES = int(data)


@ee.on("shuffle key")
def on_shuffle_key(data):
    l.proc("Shuffling key")
    shuffle(ALICE_KEY, TEMP, LEN_SHUFFLE, 0)
    update_file(TEMP, ALICE_KEY)
    l.ok()
    rh.emit("iteration ended")


@ee.on("message")
def message(args):
    l.info("New message from remote host:", args)


@ee.on("exit")
def exit(args):
    def payload():
        l.warn("Terminating by remote command...")
        sleep(1)
        _exit(0)

    Thread(target=payload).start()


def run():
    l.info("Running Alice...")
    server.set_emitter(ee)
    Thread(target=server.start).start()
    l.proc("Saying hello to Bob")
    rh.emit("message", "Hello, Bob!")
    l.ok()
