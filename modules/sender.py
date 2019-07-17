import requests


def send(address, name):
    with open(name, "rb") as content:
        print("Connecting to %s... " % address, end='')
        res = requests.post(
            url="http://%s:56583/upload?filename=%s" % (address, name),
            headers={"Content-Type": "application/octet-stream"},
            data=content.read(),
        )
        print(res.text)


def sync(address, route):
    res = requests.get("http://%s:56583/%s" % (address, route))
    return res.text
