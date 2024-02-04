from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.query import dict_factory

from flask import Flask, g

# Store prepared statements in this dictionary to use them in your queries
PREPARED_STATEMENTS = {}
# Save the keys for the dictionary as a constant 
ALL_AUTHORS = 'all_authors'

def create_app():
    app = Flask(__name__)

    with app.app_context():
        get_db_session()

    print('Connected to Scylla!')

    return app 

def get_db_session():
    if 'db' not in g:
        profile = ExecutionProfile(
            row_factory=dict_factory
        )

        cluster = Cluster(
            ["127.0.0.1"], 
            port=9042, 
            execution_profiles={EXEC_PROFILE_DEFAULT: profile}
        )

        session = cluster.connect('reviews')

        # Insert prepared queries into the dictionary when initializing
        # the database
        PREPARED_STATEMENTS[ALL_AUTHORS] = session.prepare(
            'SELECT * FROM authors'
        )

        g.db = session
    
    return g.db

app = create_app()

@app.route('/authors')
def authors():
    db = get_db_session()

    # To use a prepared statement, pass the prepared statement to 
    # the session's execute method. 
    result_set = db.execute(PREPARED_STATEMENTS[ALL_AUTHORS])

    authors = []
    for row in result_set:
        authors.append(row)

    return authors

@app.route('/') 
def hello_world(): 
    return 'ScyllaDB in Action!' 