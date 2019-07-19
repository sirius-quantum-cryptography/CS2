import requests

class RemoteHost:
    address = ''
    debug = False

    def __init__(self, address):
        self.address += 'http://' + address

    def send_file(self, path):
        with open(path, "rb") as content:
            res = requests.post(
                url=f"{self.address}/upload?filename={path.split('/')[-1]}",
                headers={"Content-Type": "application/octet-stream"},
                data=content.read()
            )
            return res.text

    def emit(self, event, args=0):
        url = f"{self.address}/emit?event={event}&args={args}"
        if self.debug:
            print(f'Connecting to {url}...')
        res = requests.get(url)
        if self.debug:
            print('Request finished, is ok:', res.ok)
        return res.text