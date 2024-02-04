from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import ConstantSpeculativeExecutionPolicy, TokenAwarePolicy, RoundRobinPolicy
from cassandra.query import BatchStatement, dict_factory

from datetime import datetime

from dataclasses import dataclass

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

SPECULATIVE_RETRY_INTERVAL = 0.1 # seconds
SPECULATIVE_RETRY_MAX_ATTEMPTS = 2

IDEMPOTENT_QUERIES = {ALL_AUTHORS, GET_ARTICLE, GET_AUTHOR}

BUCKET_START_DATE = datetime(2023, 10, 1)

@dataclass
class Image:
    path: str 
    caption: str

def create_app():
    app = Flask(__name__)

    with app.app_context():
        get_db_session()

    print('Connected to Scylla!')

    return app 

def get_db_session():
    if 'db' not in g:
        profile = ExecutionProfile(
            row_factory=dict_factory,
            load_balancing_policy=TokenAwarePolicy(RoundRobinPolicy()),
            speculative_execution_policy=ConstantSpeculativeExecutionPolicy(
                SPECULATIVE_RETRY_INTERVAL, SPECULATIVE_RETRY_MAX_ATTEMPTS
            )
        )

        # The PlainTextAuthProvider works with the PasswordAuthenticator in 
        # Scylla. 
        auth_provider = PlainTextAuthProvider(
            username='reviews_api', password='password')

        cluster = Cluster(
            ["127.0.0.1"], 
            port=9042, 
            execution_profiles={EXEC_PROFILE_DEFAULT: profile},
            # Passing the auth provider to the cluster allows you to log in
            # using the provider's credentials. 
            auth_provider=auth_provider
        )

        cluster.register_user_type('reviews', 'image', Image)
        
        session = cluster.connect('reviews')

        PREPARED_STATEMENTS[ALL_AUTHORS] = session.prepare(
            'SELECT * FROM authors'
        )

        PREPARED_STATEMENTS[GET_ARTICLE] = session.prepare(
            """
            SELECT *
            FROM articles 
            WHERE id = ?
            """
        )

        PREPARED_STATEMENTS[GET_AUTHOR] = session.prepare(
            'SELECT * FROM authors WHERE id = ?',
        )
        PREPARED_STATEMENTS[INSERT_ARTICLE] = session.prepare(
            """INSERT INTO articles(
                id, author_id, date, images, restaurant_name, review, 
                score, title
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
            )"""
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
        
        for statement in PREPARED_STATEMENTS.values():
            statement.consistency_level = ConsistencyLevel.LOCAL_QUORUM

        for key in IDEMPOTENT_QUERIES:
            PREPARED_STATEMENTS[key].is_idempotent = True 

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
    
    if row.get("images") is not None:
        row["images"] = list(row["images"])

    return row 


@app.route('/articles', methods = ['POST'])
def create_article():
    data = request.json 

    author_id = uuid.UUID(data['author_id'])

    db = get_db_session()
    author_result_set = db.execute(
        PREPARED_STATEMENTS[GET_AUTHOR], 
        [author_id],
    )

    if author_result_set is None: 
        abort(404)

    author_name = author_result_set[0]['name']

    date = data['date'] 
    restaurant_name = data['restaurant_name']
    review = data['review']
    score = data['score']
    title = data['title']

    article_date = datetime.strptime(date, '%Y-%m-%d')

    date_bucket = (article_date.year - BUCKET_START_DATE.year) * 12 + \
        article_date.month - BUCKET_START_DATE.month

    images = []

    image_data = data.get('images')

    if image_data is not None:
        for image in image_data:
            path = image['path']
            caption = image['caption']
            images.append(Image(path=path, caption=caption))

    summary_image = images[0] if len(images) > 0 else None

    if data.get('id') is None: 
        id = uuid.uuid1()
    else: 
        id = uuid.UUID(data['id'])

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

    db.execute(batch)

    article = get_article(id, db=db)

    return article 

@app.route('/') 
def hello_world(): 
    return 'ScyllaDB in Action!' 