CREATE TABLE IF NOT EXISTS raw_data (
    id BIGINT PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    user_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cleaned_data (
    id BIGINT PRIMARY KEY,
    cleaned_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    user_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS analyzed_data (
    id BIGINT PRIMARY KEY,
    sentiment TEXT NOT NULL,
    score REAL NOT NULL,
    created_at TIMESTAMP NOT NULL,
    user_name TEXT NOT NULL
);
