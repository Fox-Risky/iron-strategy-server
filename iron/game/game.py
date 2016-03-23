import asyncio
import concurrent.futures
from iron.utils.crypto import generate_random_id
from iron.utils.db import make_rdb_connection

import rethinkdb as r

from autobahn.wamp import RegisterOptions

NEW_PLAYERS_TOPIC = 'com.game.new_player'
PLAYER_ACTION_TOPIC = 'com.game.player_action'

class Game(object):

    """Game module for AutobahnPython

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
        self.tasks = []
        await self.registerGame()
        self._logger.info('Registered game methods.')
        await self.listenForGameEvents()
        self._logger.info('Listening for game events.')

    def __del__(self):
        for task in self.tasks:
            task.cancel()

    async def registerGame(self):
        methods = {
            "com.game.join": self.joinWorld
        }

        for endpoint, handler in methods.items():
            await self._session.register(handler, endpoint, options=RegisterOptions(details_arg='details'))

    async def listenForGameEvents(self):
        await self.publishPlayerChanges()

    async def publishPlayerChanges(self):
        query = await r.table('players').filter({"in_game": True}).run(self._db)

        while (await query.fetch_next()):
            item = query.next()
            new_player = item['new_val']
            if not change['old_val']['in_game'] and change['old_val']['in_game']: # New player
                self._logger.info('New player: {} joined the world!'.format(new_player['username']))
                await self._session.publish(NEW_PLAYER_TOPIC, player, { exclude: [new_player['caller_id']] })
            else:
                self._logger.info('Player: {} has done an action.'.format(new_player['username']))
                await self._session.publish(PLAYER_ACTION_TOPIC, player, { exclude: [new_player['caller_id']] })

    async def joinWorld(self, details=None):
        if details is None:
            self._logger.warn('Connection initiated without details')

        player = await r.table('players').filter({
            "caller_id": details.caller
        }).run(self._db)

        await r.table('players').filter({
            "caller_id": details.caller
        }).update({
            "in_game": True
        }).run(self._db)

        self._logger.info('{} joined the world game.'.format(player['username']))

        cur_players = await r.table('players').filter({
            "in_game": True
        }).run(self._db)

        return {
            'players': cur_players
        }
