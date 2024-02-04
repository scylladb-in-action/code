CREATE role application;
GRANT SELECT ON KEYSPACE reviews TO application;
GRANT MODIFY ON KEYSPACE reviews TO application;
CREATE ROLE reviews WITH PASSWORD = 'password' AND LOGIN = true;
GRANT application TO reviews;