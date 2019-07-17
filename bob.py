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
REMOTE_HOST += ':64295'
sio = socketio.Server()
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
    sio.emit("send parity", room=sid)


@sio.on("parity sent")
def on_parity_received(sid):
    global LEN_NES
    print('LN', LEN_NES)
    print("Parity received!")
    print("Generating bad blocks...")
    hamming_correct(BOB_KEY, PARITY, TEMP, BAD_BLOCKS, POWER, len_nes=LEN_NES // 11, drop_bad=True)
    update_file(TEMP, BOB_KEY)
    print("Shuffling key...")
    shuffle(BOB_KEY, TEMP, LEN_SHUFFLE, 0)
    update_file(TEMP, BOB_KEY)
    print("Sending badblocks... ", end='')
    send(REMOTE_HOST, BAD_BLOCKS)
    print("OK")
    LEN_NES = 0
    sio.emit("wipe badblocks", LEN_NES, room=sid)


@sio.on("blocks wiped")
def on_blocks_wiped(sid):
    print("Blocks wiped")
    sio.emit("shuffle key", room=sid)


@sio.on("iteration ended")
def on_next_iteration(sid):
    global iteration
    if iteration == 3:
        print("Finished! Closing in 10 sec")
        sleep(10)
        _exit()
    print("Next iteration...")
    iteration += 1
    sio.emit("generate parity", room=sid)


@sio.on("hello")
def hello(sid, data):
    print(f"{sid}: {data}")
    sio.emit("hello", "Hello, Alice!", room=sid)
    print("Alice is generating parity...")
    sio.emit("generate parity", room=sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


def run():
    global server
    print("Running Bob...")
    Thread(target=start_socket).start()
    Thread(target=server.start).start()
