__author__ = "mashed-potatoes"

import requests
from os import _exit
from typing import Union
from modules.logger import Logger


class RemoteHost:
    address = ""
    debug = False
    logger = None

    def __init__(self, address: str, logger: Logger):
        self.address += "http://" + address
        self.logger = logger

    def send_file(self, path: str) -> Union[str, None]:
        try:
            with open(path, "rb") as content:
                res = requests.post(
                    url=f"{self.address}/upload?filename={path.split('/')[-1]}",
                    headers={"Content-Type": "application/octet-stream"},
                    data=content.read(),
                )
                return res.text
        except Exception as e:
            self.logger.fail()
            self.logger.info(e.args[0])
            _exit(0xEE)

    def emit(self, event: str, args=0) -> Union[str, None]:
        try:
            res = requests.get(f"{self.address}/emit?event={event}&args={args}")
            return res.text
        except Exception as e:
            self.logger.fail()
            self.logger.info(e.args[0])
            _exit(0xEE)
