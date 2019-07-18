from modules.fileserver import FileServer
from threading import Thread
from time import sleep
from os import _exit
from modules.hamming import *
from modules.config import *
from modules.iohelper import update_file
from modules.sender import send
import eventlet, socketio, os

server = FileServer(64296)
REMOTE_HOST += ":64295"
sio = socketio.Server(async_handlers=True)
app = socketio.WSGIApp(sio)
iteration = 0


def start_socket():
    global app
    eventlet.wsgi.server(eventlet.listen(("", 29083)), app)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.on("parity generated")
def on_patrity_generated(sid):
    print("Alice generated parity")
    sio.emit("send parity")


@sio.on("parity sent")
def on_parity_received(sid):
    global LEN_NES
    print("Parity received!")
    print("Generating bad blocks... ", end="")
    def cringe():
        global LEN_NES
        hamming_correct(
            BOB_KEY, PARITY, TEMP, BAD_BLOCKS, POWER, len_nes=LEN_NES // 11, drop_bad=True
        )
        update_file(TEMP, BOB_KEY)
        print("OK\nShuffling key... ", end="")
        shuffle(BOB_KEY, TEMP, LEN_SHUFFLE, 0)
        update_file(TEMP, BOB_KEY)
        print("OK\nSending badblocks... ", end="")
        send(REMOTE_HOST, BAD_BLOCKS)
        print("kOK")
        LEN_NES = 0
        sio.emit("wipe badblocks", LEN_NES)
    Thread(target=cringe).start()


@sio.on("blocks wiped")
def on_blocks_wiped(sid):
    print("Blocks wiped")
    sio.emit("shuffle key")


@sio.on("iteration ended")
def on_next_iteration(sid):
    global iteration
    print(f'*** THE ITERATION {iteration + 1} of {ITERATIONS} ***')
    if iteration == ITERATIONS:
        print("Finished! Closing in 10 sec")
        sleep(10)
        _exit(0)
    print("Next iteration...")
    iteration += 1
    sio.emit("generate parity")


@sio.on("hello")
def hello(sid, data):
    global iteration
    print(f"{sid}: {data}")
    sio.emit("hello", "Hello, Alice!")
    print("Alice is generating parity...")
    sio.emit("generate parity")
    iteration += 1


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


def run():
    global server
    print("Running Bob...")
    Thread(target=start_socket).start()
    Thread(target=server.start).start()
