CREATE TABLE frozen_collections(
    text TEXT,
    list FROZEN<LIST>
    set_text FROZEN<SET<TEXT>>,
    map FROZEN<MAP<TEXT, TEXT>>
);
