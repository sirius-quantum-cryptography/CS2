import requests


def send(address, name):
    with open(name, "rb") as content:
        res = requests.post(
            url="http://%s/upload?filename=%s" % (address, name.split("/")[-1]),
            headers={"Content-Type": "application/octet-stream"},
            data=content.read(),
        )
        return res.text
