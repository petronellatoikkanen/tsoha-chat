CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    role INTEGER,
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);


CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    conversation TEXT UNIQUE,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    topic_id INTEGER REFERENCES topics
);


CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP, 
    convo_id INTEGER REFERENCES conversations,
    topic_id INTEGER REFERENCES topics
);

CREATE TABLE secret_topics (
    id SERIAL PRIMARY KEY,
    secret_topic TEXT UNIQUE,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE secret_topics_users (
    secret_topic_id INT REFERENCES secret_topics(id),
    user_id INTEGER REFERENCES users,
    PRIMARY KEY (secret_topic_id, user_id)
);

CREATE TABLE secret_messages (
    id SERIAL PRIMARY KEY,
    secret_message TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP, 
    secret_topic_id INTEGER REFERENCES secret_topics
);




 
    
