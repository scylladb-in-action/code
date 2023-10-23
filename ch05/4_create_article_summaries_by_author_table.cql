CREATE TABLE reviews.article_summaries_by_author(
    author_id TIMEUUID,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    score TINYINT,
    image image,
    PRIMARY KEY (author_id, id)
) WITH CLUSTERING ORDER BY (id DESC);