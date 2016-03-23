from logbook import StreamHandler, info
import sys
import os
import signal
import asyncio

def stop_component():
    loop = asyncio.get_event_loop()
    loop.stop()
    loop.close()
    sys.exit(0)

def initialize_component():
    StreamHandler(sys.stdout).push_application()
    info('Component logging initialized.')

    ws = sys.argv[1]
    info('Received WebSocket endpoint: {}'.format(ws))

    signal.signal(signal.SIGTERM, stop_component)
    info('SIGTERM catcher was put to shutdown the event loop gracefully.')

    return ws
