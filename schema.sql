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
    visible INTEGER DEFAULT 1;
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    convo TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
    topic_name TEXT
    visible INTEGER DEFAULT 1;
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_id INTEGER REFERENCES users,
    created TIMESTAMP,
    visible INTEGER DEFAULT 1;
);

CREATE TABLE secret_topics (
    id SERIAL PRIMARY KEY,
    secret_topic TEXT,
    creator_user_id INTEGER REFERENCES users,
    users_user_id INTEGER REFERENCES users,
    created TIMESTAMP,
    visible INTEGER DEFAULT 1;
);
