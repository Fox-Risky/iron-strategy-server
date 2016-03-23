import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))
from iron.utils.initialization import initialize_component

from autobahn.asyncio.wamp import ApplicationRunner
from iron.game.session import AppSession
# from utils.secrets import read_secret

import sys

def main():
    ws = initialize_component()
    # secret = read_secret()
    runner = ApplicationRunner(ws, u"realm1")
    runner.run(AppSession)

if __name__ == '__main__':
    main()
