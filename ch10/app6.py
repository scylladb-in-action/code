from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT

# BatchStatement allows you to perform batch writes to the cluster
from cassandra.query import BatchStatement, dict_factory

# datetime is imported to help calculate summaries' date buckets
from datetime import datetime

# The request is also imported from Flask to access the response body
from flask import Flask, abort, g, request

import uuid

PREPARED_STATEMENTS = {}
ALL_AUTHORS = 'all_authors'
GET_ARTICLE = 'get_article'
GET_AUTHOR = 'get_author'
INSERT_ARTICLE = 'insert_article'
INSERT_ARTICLE_SUMMARIES_BY_AUTHOR = 'insert_article_summaries_by_author'
INSERT_ARTICLE_SUMMARIES_BY_DATE = 'insert_article_summaries_by_date'
INSERT_ARTICLE_SUMMARIES_BY_SCORE = 'insert_article_summaries_by_score'

# Setting the bucket start date as a constant allows you to easily
# calculate the current date bucket 
BUCKET_START_DATE = datetime(2023, 10, 1)

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

        PREPARED_STATEMENTS[ALL_AUTHORS] = session.prepare(
            'SELECT * FROM authors'
        )
        PREPARED_STATEMENTS[GET_ARTICLE] = session.prepare(
            """
            SELECT id, author_id, date, restaurant_name, review, 
                score, title 
            FROM articles 
            WHERE id = ?
            """
        )
        PREPARED_STATEMENTS[GET_AUTHOR] = session.prepare(
            'SELECT * FROM authors WHERE id = ?'
        )
        PREPARED_STATEMENTS[INSERT_ARTICLE] = session.prepare(
            """INSERT INTO articles(
                id, author_id, date, images, restaurant_name, review, 
                score, title
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
            )""" # eight question marks, one for each column
        )
        PREPARED_STATEMENTS[INSERT_ARTICLE_SUMMARIES_BY_AUTHOR] = session.prepare(
                """INSERT INTO article_summaries_by_author(
                    author_id, id, author_name, image, score, title
                ) VALUES (
                    ?, ?, ?, ?, ?, ?
                )""" 
            )
        PREPARED_STATEMENTS[INSERT_ARTICLE_SUMMARIES_BY_DATE] = session.prepare(
                """INSERT INTO article_summaries_by_date(
                    date_bucket, id, author_name, image, score, title
                ) VALUES (
                    ?, ?, ?, ?, ?, ?
                )""" 
            )
        PREPARED_STATEMENTS[INSERT_ARTICLE_SUMMARIES_BY_SCORE] = session.prepare(
                """INSERT INTO article_summaries_by_score(
                    score, id, author_name, image, title
                ) VALUES (
                    ?, ?, ?, ?, ?
                )""" 
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

@app.route('/articles/<id>')
def articles(id):
    return get_article(uuid.UUID(id))

# Defaulting the db to None allows you to pass in an already-existing
# session if you happen to have one. 
def get_article(id, db=None):
    if db is None:
        db = get_db_session() 

    result_set = db.execute(
        PREPARED_STATEMENTS[GET_ARTICLE], 
        [id]
    )

    if result_set is None: 
        abort(404)
    
    row = result_set[0]

    if row.get("date") is not None:
        row["date"] = row["date"].date().strftime('%Y-%m-%d')

    return row 


@app.route('/articles', methods = ['POST'])
def create_article():
    data = request.json 

    # Convert the author ID from the request into a UUID 
    author_id = uuid.UUID(data['author_id'])

    # Retrieve the author so that you can get their name
    db = get_db_session()
    author_result_set = db.execute(
        PREPARED_STATEMENTS[GET_AUTHOR], 
        [author_id]
    )

    # If the author doesn't exist, return an error to the caller
    if author_result_set is None: 
        abort(404)

    author_name = author_result_set[0]['name']

    date = data['date'] 
    restaurant_name = data['restaurant_name']
    review = data['review']
    score = data['score']
    title = data['title']

    # Convert the date into a datetime to prepare to calculate the bucket 
    article_date = datetime.strptime(date, '%Y-%m-%d')

    # Calculate the date bucket by determining the number of months since
    # the bucket start date 
    date_bucket = (article_date.year - BUCKET_START_DATE.year) * 12 + \
        article_date.month - BUCKET_START_DATE.month

    # Placeholders for now. 
    images = []
    summary_image = None

    # Generate an article ID
    id = uuid.uuid1()

    # To perform a batch query, construct a batch statement and 
    # add each of your prepared statements to the batch.
    batch = BatchStatement()
    batch.add(
        PREPARED_STATEMENTS[INSERT_ARTICLE], 
        [id, author_id, date, images, restaurant_name, review, score, title]
    )
    batch.add(
        PREPARED_STATEMENTS[INSERT_ARTICLE_SUMMARIES_BY_AUTHOR],
        [author_id, id, author_name, summary_image, score, title]
    )
    batch.add(
        PREPARED_STATEMENTS[INSERT_ARTICLE_SUMMARIES_BY_DATE],
        [date_bucket, id, author_name, summary_image, score, title]
    )
    batch.add(
        PREPARED_STATEMENTS[INSERT_ARTICLE_SUMMARIES_BY_SCORE],
        [score, id, author_name, summary_image, title]
    )

    # Once all queries have been added, you're free to execute the
    # batch.
    db.execute(batch)

    # Load the article from the database to return to the user. 
    article = get_article(id, db=db)

    return article 

@app.route('/') 
def hello_world(): 
    return 'ScyllaDB in Action!' 