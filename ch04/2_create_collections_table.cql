CREATE TABLE collections(
    text TEXT,
    list LIST<TEXT>,
    set_text SET<TEXT>, 
    map MAP<TEXT, TEXT>,
    PRIMARY KEY (text)
);
