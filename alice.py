from modules.fileserver import FileServer

server = FileServer(64295)

def run():
    global server
    server.start()
    print('Running Alice...')
