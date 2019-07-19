class Logger:
    active = False

    def proc(self, message):
        if self.active:
            self.ok()
        self.active = True
        print(f"[....] {message}", end="\r")

    def info(self, message):
        print(f"[\033[94mINFO\033[0m] {message}")

    def warn(self, message):
        print(f"[\033[93mWARN\033[0m] {message}")

    def ok(self):
        if not self.active:
            return
        self.active = False
        print("[\033[92m OK \033[0m")

    def fail(self):
        if not self.active:
            return
        self.active = False
        print(f"[\033[91mFAIL\033[0m")
