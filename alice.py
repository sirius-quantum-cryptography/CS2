from threading import Thread
from os import _exit
from modules.config import *
from modules.hamming import *
from modules.sender import RemoteHost
from modules.iohelper import update_file
from modules.http_server import NetIO
from pymitter import EventEmitter

ee = EventEmitter()
server = NetIO(64295)
rh = RemoteHost(REMOTE_HOST)


@ee.on("generate parity")
def on_generate_parity(data):
    print("Generating parity... ", end="")
    hamming_parity(ALICE_KEY, PARITY, POWER, LEN_NES)
    rh.emit("parity generated")
    print("OK")


@ee.on("send parity")
def on_parity_requested(data):
    print("Sending parity... ", end="")
    rh.send_file(PARITY)
    print("OK\nWaiting for a Bob... ", end="")
    rh.emit("parity sent")


@ee.on("wipe badblocks")
def on_wipe_badblocks(data):
    global LEN_NES
    print("OK\nWiping badblocks... ", end="")
    hamming_wipe(ALICE_KEY, TEMP, BAD_BLOCKS, POWER, len_nes=LEN_NES // 11)
    update_file(TEMP, ALICE_KEY)
    print("OK")
    rh.emit("blocks wiped")
    LEN_NES = int(data)


@ee.on("shuffle key")
def on_shuffle_key(data):
    print("Shuffling key... ", end="")
    shuffle(ALICE_KEY, TEMP, LEN_SHUFFLE, 0)
    update_file(TEMP, ALICE_KEY)
    print("OK")
    rh.emit("iteration ended")


@ee.on("message")
def message(args):
    print("New message from remote host:", args)


@ee.on('exit')
def exit(args):
    def payload():
        print('Terminating by remote command...')
        sleep(1)
        _exit(0)
    Thread(target=payload).start()


def run():
    print("Running Alice...")
    server.set_emitter(ee)
    Thread(target=server.start).start()
    print("Saying hello to Bob")
    rh.emit("message", "Hello, Bob!")
