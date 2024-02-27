from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.query import dict_factory

from flask import Flask, abort, g

import uuid

PREPARED_STATEMENTS = {}
ALL_AUTHORS = 'all_authors'
GET_ARTICLE = 'get_article'

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
            port=19042, 
            execution_profiles={EXEC_PROFILE_DEFAULT: profile}
        )

        session = cluster.connect('reviews')

        PREPARED_STATEMENTS[ALL_AUTHORS] = session.prepare(
            'SELECT * FROM authors'
        )

        # Adding a prepared statement to load an article. Skip loading
        # images here to simplify the example. 
        PREPARED_STATEMENTS[GET_ARTICLE] = session.prepare(
            """
            SELECT id, author_id, date, restaurant_name, review, 
                score, title 
            FROM articles 
            WHERE id = ?
            """
        )

        g.db = session
    
    return g.db

app = create_app()

@app.route('/authors')
def authors():
    db = get_db_session()
    result_set = db.execute(PREPARED_STATEMENTS[ALL_AUTHORS])

    authors = []
    for row in result_set:
        authors.append(row)

    return authors

# By including id in brackets, you're able to access it as a 
# method parameter.
@app.route('/articles/<id>')
def articles(id):
    db = get_db_session()

    # You execute the prepared statement to read the article.
    result_set = db.execute(
        PREPARED_STATEMENTS[GET_ARTICLE], 

        # Passing in the ID (and converting it to a UUID) binds the ID
        # to the ? parameter inside the prepared statement.
        [uuid.UUID(id)]
    )

    # If you find nothing, return a 404
    if result_set is None:
        abort(404)

    # There should be only one row in the result set since you're querying
    # by the full primary key.
    row = result_set[0]

    # When reading from a database, you frequently need to convert data.
    # Here, you convert the database's date into a date string that
    # serializes correctly. 
    if row.get("date") is not None:
        row["date"] = row["date"].date().strftime('%Y-%m-%d')

    return row 

@app.route('/') 
def hello_world(): 
    return 'ScyllaDB in Action!' 