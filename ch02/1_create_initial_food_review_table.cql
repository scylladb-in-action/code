CREATE TABLE initial.food_reviews ( 
    restaurant text, 
    ordered_at timestamp, 
    food text,
    review text,
    PRIMARY KEY (restaurant, ordered_at, food) 
);
