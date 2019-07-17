import requests


def send(address, name):
    with open(name, "rb") as content:
        print("Connecting to %s... " % address, end="")
        res = requests.post(
            url="http://%s/upload?filename=%s" % (address, name.split('/')[-1]),
            headers={"Content-Type": "application/octet-stream"},
            data=content.read(),
        )
        print(res.text)
