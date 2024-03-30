CREATE KEYSPACE stress WITH replication = {
    'class': 'NetworkTopologyStrategy', 'datacenter1': '1'};

CREATE TYPE stress.image(
    path TEXT,
    caption TEXT,
);

CREATE TABLE stress.articles(
    id TIMEUUID,
    title TEXT,
    author_id TIMEUUID,
    score TINYINT,
    date DATE,
    review TEXT,
    restaurant_name TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE stress.article_summaries_by_author(
    author_id TIMEUUID,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    score TINYINT,
    PRIMARY KEY (author_id, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE stress.article_summaries_by_date(
    date_bucket SMALLINT,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    score TINYINT,
    PRIMARY KEY (date_bucket, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE stress.article_summaries_by_score(
    score TINYINT,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    PRIMARY KEY (score, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE stress.authors(
    id TIMEUUID,
    name TEXT,
    bio TEXT,
    PRIMARY KEY (id)
);

