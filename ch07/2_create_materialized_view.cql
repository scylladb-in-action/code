CREATE MATERIALIZED VIEW 
    reviews.article_summaries_by_score_view
    AS 
        SELECT score, id, title, author_name, image
        FROM article_summaries_by_date
        WHERE score IS NOT NULL
          AND date_bucket IS NOT NULL 
          AND id IS NOT NULL 
    PRIMARY KEY(score, date_bucket, id);
