CREATE TABLE reviews.article_summaries_by_score(
    score TINYINT,
    id TIMEUUID,
    title TEXT,
    author_name TEXT,
    image image,
    PRIMARY KEY (score, id)
);
