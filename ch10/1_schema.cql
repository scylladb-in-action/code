CREATE KEYSPACE reviews WITH replication = {
    'class': 'NetworkTopologyStrategy', 'datacenter1': '1'};

CREATE TYPE reviews.image(
    path TEXT,
    caption TEXT,
);

CREATE TABLE reviews.articles(
    id TIMEUUID,
    title TEXT,
    author_id TIMEUUID,
    score TINYINT,
    date DATE,
    images SET<FROZEN<image>>,
    review TEXT,
    restaurant_name TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE reviews.article_summaries_by_author(
    author_id TIMEUUID,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    score TINYINT,
    image image,
    PRIMARY KEY (author_id, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE reviews.article_summaries_by_date(
    date_bucket SMALLINT,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    score TINYINT,
    image image,
    PRIMARY KEY (date_bucket, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE reviews.article_summaries_by_score(
    score TINYINT,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    image image,
    PRIMARY KEY (score, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE TABLE reviews.authors(
    id TIMEUUID,
    name TEXT,
    bio TEXT,
    image image,
    PRIMARY KEY (id)
);

