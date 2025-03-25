CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INTEGER,
    sex VARCHAR(6)
);

CREATE TABLE swipes (
    id1 INTEGER,
    id2 INTEGER,
    swipe1 BOOLEAN DEFAULT False,
    swipe2 BOOLEAN DEFAULT False
);
