from autobahn.asyncio.wamp import ApplicationSession

from iron.game.game import Game
from iron.utils.logging import make_logger
from iron.utils.db import make_rdb_connection
from iron.utils.config import open_server_config

class AppSession(ApplicationSession):

    log = make_logger('Game')
    game = Game()
    user_config = open_server_config()
    db = None

    async def onJoin(self, details):
        self.log.info("Game module joined the router.")
        self.db = await make_rdb_connection(self.user_config)
        self.log.info("Game module connected to the database.")
        await self.game.start(self, self.log, self.db, self.user_config)
        self.log.info("Game module is ready.")
