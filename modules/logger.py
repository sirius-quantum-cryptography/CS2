__author__ = "mashed-potatoes"

class Logger:
    active = False

    def proc(self, message: str, points=-1) -> None:
        if self.active:
            self.ok()
        if points == -1:
            points = 6
        self.active = True
        print(f"[{'.' * points}{' ' * (6 - points)}] {message}", end="\r")

    def info(self, message: str) -> None:
        print(f"[\033[94m INFO \033[0m] {message}")

    def warn(self, message: str) -> None:
        print(f"[\033[93m WARN \033[0m] {message}")

    def ok(self) -> None:
        if not self.active:
            return
        self.active = False
        print("[\033[92m  OK  \033[0m]")

    def fail(self) -> None:
        if not self.active:
            return
        self.active = False
        print(f"[\033[91m FAIL \033[0m]")
