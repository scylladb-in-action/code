TRUNCATE reviews.authors;

INSERT INTO reviews.authors(
  id, 
  name, 
  bio 
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2, 
  'Alice Author',
  'Alice loves writing about food'
); 

INSERT INTO reviews.authors(
  id,
  name,
  bio
) VALUES (
  33a753de-704c-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  'Reginald is a food enthusiast who loves to review food'
);

CREATE TABLE IF NOT EXISTS reviews.article_scores_by_author(
    author_id TIMEUUID,
    score TINYINT,
    id TIMEUUID,
    PRIMARY KEY (author_id, score, id)
) WITH CLUSTERING ORDER BY (score DESC, id DESC);

TRUNCATE reviews.articles;
TRUNCATE reviews.article_summaries_by_date;
TRUNCATE reviews.article_summaries_by_score;
TRUNCATE reviews.article_summaries_by_author;
TRUNCATE reviews.article_scores_by_author;

BEGIN BATCH
INSERT INTO reviews.articles(
  id,
  title,
  author_id,
  score,
  date,
  images,
  review,
  restaurant_name
) VALUES (
  1e24e04c-7044-11ee-b962-0242ac120002,
  'Ernie''s Eats Exceeds Expectations',
  1e24e04c-7044-11ee-b962-0242ac120002, 
  100,
  '2023-10-21',
  {{path: 'ernie.jpg', caption: 'Ernie, the eponymous proprietor of Ernie''s Eats'}}, 
  'I expected it to be good; it was great! At Ernie''s Eats...',
  'Ernie''s Eats'
);
INSERT INTO reviews.article_summaries_by_author(
  author_id,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2,
  1e24e04c-7044-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'ernie.jpg', caption: 'Ernie, the eponymous proprietor of Ernie''s Eats'},
  100,
  'Ernie''s Eats Exceeds Expectations'
);
INSERT INTO reviews.article_summaries_by_date(
  date_bucket,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  0,
  1e24e04c-7044-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'ernie.jpg', caption: 'Ernie, the eponymous proprietor of Ernie''s Eats'},
  100,
  'Ernie''s Eats Exceeds Expectations'
);
INSERT INTO reviews.article_summaries_by_score(
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  1e24e04c-7044-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'ernie.jpg', caption: 'Ernie, the eponymous proprietor of Ernie''s Eats'},
  100,
  'Ernie''s Eats Exceeds Expectations'
);
INSERT INTO reviews.article_scores_by_author(
  author_id,
  score,
  id
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2,
  100,
  1e24e04c-7044-11ee-b962-0242ac120002
);
APPLY BATCH;

BEGIN BATCH
INSERT INTO reviews.articles(
  id,
  title,
  author_id,
  score,
  date,
  images,
  review,
  restaurant_name
) VALUES (
  78fb3d92-7047-11ee-b962-0242ac120002,
  'Good Tacos at Main Street Tacos',
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2, 
  85,
  '2023-10-24',
  {{path: 'tortilla.jpg', caption: 'Corn tortillas'}}, 
  'Homemade tortillas make the difference...',
  'Main Street Tacos'
);
INSERT INTO reviews.article_summaries_by_author(
  author_id,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2,
  78fb3d92-7047-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'tortilla.jpg', caption: 'Corn tortillas'},
  85,
  'Good Tacos at Main Street Tacos'
);
INSERT INTO reviews.article_summaries_by_date(
  date_bucket,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  0,
  78fb3d92-7047-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'tortilla.jpg', caption: 'Corn tortillas'},
  85,
  'Good Tacos at Main Street Tacos'
);
INSERT INTO reviews.article_summaries_by_score(
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  78fb3d92-7047-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'tortilla.jpg', caption: 'Corn tortillas'},
  85,
  'Good Tacos at Main Street Tacos'
);
INSERT INTO reviews.article_scores_by_author(
  author_id,
  score,
  id
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2,
  85,
  78fb3d92-7047-11ee-b962-0242ac120002
);
APPLY BATCH;

BEGIN BATCH
INSERT INTO reviews.articles(
  id,
  title,
  author_id,
  score,
  date,
  images,
  review,
  restaurant_name
) VALUES (
  b71e77f8-704a-11ee-b962-0242ac120002,
  'Lack of Variety at Pepperoni Pizza Only',
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2, 
  75,
  '2023-10-25',
  {{path: 'pizza.jpg', caption: 'The only item on the menu'}}, 
  'They only serve one item at Pepperoni Pizza Only, but it''s pretty good...',
  'Pepperoni Pizza Only'
);
INSERT INTO reviews.article_summaries_by_author(
  author_id,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2,
  b71e77f8-704a-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'pizza.jpg', caption: 'The only item on the menu'},
  75,
  'Lack of Variety at Pepperoni Pizza Only'
);
INSERT INTO reviews.article_summaries_by_date(
  date_bucket,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  0,
  b71e77f8-704a-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'pizza.jpg', caption: 'The only item on the menu'},
  75,
  'Lack of Variety at Pepperoni Pizza Only'
);
INSERT INTO reviews.article_summaries_by_score(
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  b71e77f8-704a-11ee-b962-0242ac120002,
  'Alice Author',
  {path: 'pizza.jpg', caption: 'The only item on the menu'},
  75,
  'Lack of Variety at Pepperoni Pizza Only'
);
INSERT INTO reviews.article_scores_by_author(
  author_id,
  score,
  id
) VALUES (
  eff9bd01-4a73-11ee-8863-c02b3f99d2b2,
  75,
  b71e77f8-704a-11ee-b962-0242ac120002
);
APPLY BATCH;

BEGIN BATCH
INSERT INTO reviews.articles(
  id,
  title,
  author_id,
  score,
  date,
  images,
  review,
  restaurant_name
) VALUES (
  9f545786-704b-11ee-b962-0242ac120002,
  'Life-changing Potatoes',
  33a753de-704c-11ee-b962-0242ac120002,
  100,
  '2023-10-27',
  {{path: 'potatoes.jpg', caption: 'Mash ''em up!'}}, 
  'Without a doubt, the best mashed potatoes in this city...',
  'Mash Rules Everything Around Me'
);
INSERT INTO reviews.article_summaries_by_author(
  author_id,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  33a753de-704c-11ee-b962-0242ac120002,
  9f545786-704b-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  {path: 'potatoes.jpg', caption: 'Mash ''em up!'},
  100,
  'Life-changing Potatoes'
);
INSERT INTO reviews.article_summaries_by_date(
  date_bucket,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  0,
  9f545786-704b-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  {path: 'potatoes.jpg', caption: 'Mash ''em up!'},
  100,
  'Life-changing Potatoes'
);
INSERT INTO reviews.article_summaries_by_score(
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  9f545786-704b-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  {path: 'potatoes.jpg', caption: 'Mash ''em up!'},
  100,
  'Life-changing Potatoes'
);
INSERT INTO reviews.article_scores_by_author(
  author_id,
  score,
  id
) VALUES (
  33a753de-704c-11ee-b962-0242ac120002,
  100,
  9f545786-704b-11ee-b962-0242ac120002
);
APPLY BATCH;

BEGIN BATCH
INSERT INTO reviews.articles(
  id,
  title,
  author_id,
  score,
  date,
  images,
  review,
  restaurant_name
) VALUES (
  7fcf4e82-704d-11ee-b962-0242ac120002,
  'So Many Flavors at 9000 wings',
  33a753de-704c-11ee-b962-0242ac120002,
  90,
  '2023-10-27',
  {{path: 'wings.jpg', caption: 'They claim to have 9000 flavors'}}, 
  'They claim to have 9000 flavors, and allof them I tried were good...',
  '9000 wings'
);
INSERT INTO reviews.article_summaries_by_author(
  author_id,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  33a753de-704c-11ee-b962-0242ac120002,
  7fcf4e82-704d-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  {path: 'wings.jpg', caption: 'They claim to have 9000 flavors'},
  90,
  'So Many Flavors at 9000 wings'
);
INSERT INTO reviews.article_summaries_by_date(
  date_bucket,
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  0,
  7fcf4e82-704d-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  {path: 'wings.jpg', caption: 'They claim to have 9000 flavors'},
  90,
  'So Many Flavors at 9000 wings'
);
INSERT INTO reviews.article_summaries_by_score(
  id,
  author_name,
  image,
  score,
  title
) VALUES (
  7fcf4e82-704d-11ee-b962-0242ac120002,
  'Reginald Reviewer',
  {path: 'wings.jpg', caption: 'They claim to have 9000 flavors'},
  90,
  'So Many Flavors at 9000 wings'
);
INSERT INTO reviews.article_scores_by_author(
  author_id,
  score,
  id
) VALUES (
  33a753de-704c-11ee-b962-0242ac120002,
  90,
  7fcf4e82-704d-11ee-b962-0242ac120002
);
APPLY BATCH;
