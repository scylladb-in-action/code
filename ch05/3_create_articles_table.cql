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
