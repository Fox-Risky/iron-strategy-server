from autobahn.asyncio.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

from iron.auth.auth import Authentication
from iron.utils.logging import make_logger
from iron.utils.db import make_rdb_connection
from iron.utils.config import open_server_config

class AppSession(ApplicationSession):

    log = make_logger('Authentication')
    auth = Authentication()
    user_config = open_server_config()
    db = None

    async def onJoin(self, details):
        self.log.info("Auth module joined the router.")
        self.db = await make_rdb_connection(self.user_config)
        self.log.info("Auth module connected to the database.")
        await self.auth.start(self, self.log, self.db, self.user_config)
        self.log.info("Auth module is ready.")
