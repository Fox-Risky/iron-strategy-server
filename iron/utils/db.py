import rethinkdb as r
from logbook import error

r.set_loop_type('asyncio')

def make_rdb_connection(config):
    try:
        db_config = config['database']

        args = dict(db_config.items())
        args.update({
            'host': db_config['host'],
            'port': db_config.get('port', 28015),
            'db': db_config.get('db', 'iron-strategy')
        })

        return r.connect(**args)
    except KeyError as e:
        error('Config error: could not find key: {}'.format(e))
    except Exception as e:
        error('Could not establish the database connection: {}'.format(e))
