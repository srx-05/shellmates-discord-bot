CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'manager', 'member')) DEFAULT 'member',
    join_date TIMESTAMP,
    points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    is_banned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    event_id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    created_by TEXT REFERENCES users(user_id),
    channel_id TEXT,
    message_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event_reminders (
    reminder_id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(event_id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(user_id),
    remind_before INTEGER,
    sent BOOLEAN DEFAULT FALSE
);

CREATE TABLE cyber_facts (
    fact_id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source_type TEXT CHECK(source_type IN ('user', 'external')) DEFAULT 'user',
    source_url TEXT,
    added_by TEXT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz (
    quiz_id BIGSERIAL PRIMARY KEY,
    fact_id BIGINT REFERENCES cyber_facts(fact_id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answers TEXT,
    difficulty TEXT CHECK(difficulty IN ('easy','medium','hard')) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_results (
    result_id BIGSERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id),
    quiz_id BIGINT REFERENCES quiz(quiz_id),
    is_correct BOOLEAN,
    points_earned INTEGER DEFAULT 0,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE commands (
    command_name TEXT PRIMARY KEY,
    description TEXT,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP
    category TEXT DEFAULT 'General'

);

CREATE TABLE banned_words (
    word_id BIGSERIAL PRIMARY KEY,
    word TEXT UNIQUE NOT NULL,
    added_by TEXT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE points_history (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT REFERENCES users(user_id),
    reason TEXT,
    points_added INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW leaderboard AS
SELECT username, role, points, level
FROM users
ORDER BY points DESC, level DESC;
