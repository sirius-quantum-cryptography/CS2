__author__ = "mashed-potatoes"

class Logger:
    active = False

    def proc(self, message: str, points=4) -> None:
        if self.active and points == 4:
            self.ok()
        self.active = True
        print(f"[{'.' * points}{' ' * (4 - points)}] {message}", end="\r")

    def info(self, message: str) -> None:
        print(f"[\033[94mINFO\033[0m] {message}")

    def warn(self, message: str) -> None:
        print(f"[\033[93mWARN\033[0m] {message}")

    def ok(self) -> None:
        if not self.active:
            return
        self.active = False
        print("[\033[92m OK \033[0m")

    def fail(self) -> None:
        if not self.active:
            return
        self.active = False
        print(f"[\033[91mFAIL\033[0m")
