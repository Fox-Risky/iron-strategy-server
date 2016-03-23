import asyncio
from iron.utils.crypto import generate_random_id
from iron.utils.db import make_rdb_connection

import rethinkdb as r

from autobahn.wamp import RegisterOptions

class Authentication(object):

    """Authentication module for AutobahnPython

    Manage registration of all RPC methods and subscriptions.
    """

    def __init__(self):
        """Instantiate a auth module"""
        self._session = None
        self._logger = None
        self._db = None

    async def start(self, session, logger, db, config):
        self._session = session
        self._logger = logger
        self._db = db
        await self.registerAuthentication()
        await asyncio.sleep(1)
        await self._session.call('com.auth.initiate', 'RaitoBezarius')

    async def registerAuthentication(self):
        methods = {
            "com.auth.initiate": self.initiateConnection
        }

        for endpoint, handler in methods.items():
            await self._session.register(handler, endpoint, options=RegisterOptions(details_arg='details'))

    async def initiateConnection(self, username, details=None):
        if details is None:
            self._logger.warn('Connection initiated without details')

        connection_token = generate_random_id()
        self._logger.info('Connection initiated as {}, here is his token: {} (details: {})!'.format(username, connection_token, details))

        players = await r.table('players').filter({
            "username": username
        }).count().run(self._db)

        if players > 0:
            self._logger.debug('The username {} is already taken: {} (player: {})'.format(username, details.caller, players))
            return None

        await r.table('players').insert({
            "player_id": connection_token,
            "caller_id": details.caller,
            "username": username
        }, { upsert: True }).run(self._db)

        self._logger.info('{} joined the game!'.format(username))

        return connection_token
