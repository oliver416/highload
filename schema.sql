CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INTEGER,
    sex VARCHAR(6)
);

CREATE TABLE swipes (
    id1 INTEGER,
    id2 INTEGER,
    swipe1 BOOLEAN DEFAULT NULL,
    swipe2 BOOLEAN DEFAULT NULL,
    PRIMARY KEY (id1, id2)
);

CREATE TABLE preferences (
    id INTEGER,
    age INTEGER,
    sex VARCHAR(6),
    FOREIGN KEY (id) REFERENCES profiles (id) ON DELETE CASCADE
);
