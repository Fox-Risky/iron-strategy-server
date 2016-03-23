import sys
import os
sys.path.append(os.path.abspath('..'))

import asyncio
import rethinkdb as r
from iron.utils.config import open_server_config
from iron.utils.db import make_rdb_connection

async def create_or_drop_table(db, tables, table, **args):
    if table in tables:
        print ('Dropping old table: {}'.format(table))
        await r.table_drop(table).run(db)

    print ('Creating new table: {}'.format(table))
    await r.table_create(table, **args).run(db)

async def execute(queries):
    for query in queries:
        await query

async def create_or_upgrade():
    config = open_server_config()
    print ('Opening new db connection')
    db = await make_rdb_connection(config)

    print ('Getting tables list...')
    tables = await r.table_list().run(db)
    print ('Here are all tables: {}'.format(', '.join(tables)))
    await create_or_drop_table(db, tables, "players")
    print ('All tables were updated / created.')

    await db.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_or_upgrade())
    loop.close()
