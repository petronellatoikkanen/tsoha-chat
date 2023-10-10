CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP, 
    convo_name TEXT,
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    convo TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
    topic_name TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_id INTEGER REFERENCES users,
    created TIMESTAMP,
    visible INTEGER
);
