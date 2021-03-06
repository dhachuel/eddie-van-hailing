import rethinkdb as rdb
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import os


# RDB_HOST = 'localhost'
# RDB_PORT = 28015
RDB_HOST = 'aws-us-east-1-portal.32.dblayer.com'
RDB_PORT = 25889
RDB_USER = 'dhachuel'

# Database and table
global PROJECT_DB, PROJECT_TABLES
PROJECT_DB = 'eddie'
PROJECT_TABLES = [
    'riders',
    'quotes',
    'drivers',
    'trips',
    'sessions'
]

# Set up db connection client
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
rdb_conn = rdb.connect(
	host=RDB_HOST,
    port=RDB_PORT,
    user=RDB_USER,
    ssl={'ca_certs': os.path.join(__location__, 'cacert.crt')}
)

# Function is for cross-checking database and tables exist
def dbSetup(project_db, project_tables):
    try:
        rdb.db_create(project_db).run(rdb_conn)
        print('Database setup completed.')
    except RqlRuntimeError:
        print("{} database exists.".format(project_db))
    for table in project_tables:
        try:
            rdb.db(project_db).table_create(table).run(rdb_conn)
            print('Table <{}> creation completed'.format(table))
        except:
            print('Table <{}> already exists.'.format(table))

dbSetup(PROJECT_DB, PROJECT_TABLES)