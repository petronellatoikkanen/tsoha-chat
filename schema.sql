CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    content TEXT,
    created_at INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_id INTEGER REFERENCES users,
    created TIMESTAMP,
    visible INTEGER
);
