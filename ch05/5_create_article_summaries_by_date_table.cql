CREATE TABLE reviews.article_summaries_by_date(
    date_bucket SMALLINT,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    score TINYINT,
    image image,
    PRIMARY KEY (date_bucket, id)
) WITH CLUSTERING ORDER BY (id DESC);