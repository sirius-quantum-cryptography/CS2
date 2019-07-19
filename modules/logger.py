class Logger:
    def proc(message):
        print(f'[....] {message}', end='\r')

    def info(message):
        print(f'[\033[94mINFO\033[0m] {message}')

    def warn(message):
        print(f'[\033[93mWARN\033[0m] {message}')

    def ok():
        print('[\033[92m OK\033[0m')

    def fail():
        print(f'[\033[91mFAIL\033[0m]')