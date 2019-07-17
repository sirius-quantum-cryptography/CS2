from modules.fileserver import FileServer
from threading import Thread
import eventlet, socketio

server = FileServer(64296)
sio = socketio.Server()
app = socketio.WSGIApp(sio)

def start_socket():
    global app
    eventlet.wsgi.server(eventlet.listen(('', 29083)), app)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def run():
    global server
    print('Running Bob...')
    Thread(target=start_socket).start()
    Thread(target=server.start).start()
