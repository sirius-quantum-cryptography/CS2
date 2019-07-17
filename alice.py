from modules.fileserver import FileServer
from threading import Thread
from os import _exit
from time import sleep
from modules.config import *
from modules.hamming import *
from modules.sender import send
from modules.iohelper import update_file
import socketio

sio = socketio.Client()
server = FileServer(64295)


@sio.on("generate parity")
def on_generate_parity(data):
    print("Generating parity... ", end="")
    hamming_parity(ALICE_KEY, PARITY, POWER, LEN_NES)
    sio.emit("parity generated")
    print("OK")


@sio.on("send parity")
def on_parity_requested(data):
    print("Sending parity... ", end="")
    send(REMOTE_HOST, PARITY)
    print("OK\nWaiting for a Bob... ", end="")
    sio.emit("parity sent")


@sio.on("wipe badblocks")
def on_wipe_badblocks(data):
    global LEN_NES
    print("OK\nWiping badblocks... ", end="")
    hamming_wipe(ALICE_KEY, TEMP, BAD_BLOCKS, POWER, len_nes=LEN_NES // 11)
    update_file(TEMP, ALICE_KEY)
    print("OK")
    sio.emit("blocks wiped")
    LEN_NES = data


@sio.on("shuffle key")
def on_shuffle_key(data):
    print("Shuffling key... ", end="")
    shuffle(ALICE_KEY, TEMP, LEN_SHUFFLE, 0)
    update_file(TEMP, ALICE_KEY)
    print("OK")
    sio.emit("iteration ended")


@sio.on("hello")
def message(data):
    print("I received a message: %s" % data)


@sio.event
def connect():
    print("I'm connected to Bob!")


@sio.event
def disconnect():
    print("I'm disconnected! Exiting...")
    _exit(0)


def connect_to_bob():
    global sio, REMOTE_HOST
    sio.connect("http://%s:29083" % REMOTE_HOST)
    REMOTE_HOST += ":64296"
    print("My sid is", sio.sid)


def run():
    global server
    Thread(target=server.start).start()
    print("Running Alice...")
    connect_to_bob()
    print("Saying hello to Bob")
    sio.emit("hello", "Hello, Bob!")
