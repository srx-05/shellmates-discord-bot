
-- 1. USERS ENTITY

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    discord_id VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_discord_id ON users(discord_id);
CREATE INDEX idx_users_joined_at ON users(joined_at);

-- 2. ADMINS TABLE

CREATE TABLE admins (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL DEFAULT 'moderator',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(user_id)
);


CREATE INDEX idx_admins_user_id ON admins(user_id);
CREATE INDEX idx_admins_role ON admins(role);

-- 3. PERMISSIONS TABLE

CREATE TABLE permissions (
    id BIGSERIAL PRIMARY KEY,
    admin_id BIGINT NOT NULL REFERENCES admins(id) ON DELETE CASCADE,
    module VARCHAR(100) NOT NULL,
    can_create BOOLEAN DEFAULT FALSE,
    can_read BOOLEAN DEFAULT TRUE,
    can_update BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(admin_id, module)
);

CREATE INDEX idx_permissions_admin_id ON permissions(admin_id);
CREATE INDEX idx_permissions_module ON permissions(module);


-- 4. EVENTS TABLE

CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    location VARCHAR(255),
    created_by BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    status VARCHAR(50) DEFAULT 'upcoming',
    max_participants INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_event_date ON events(event_date);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_created_by ON events(created_by);



-- 5. EVENT ATTENDANCE TABLE

CREATE TABLE event_attendance (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending',
    responded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, user_id)
);

CREATE INDEX idx_attendance_event_id ON event_attendance(event_id);
CREATE INDEX idx_attendance_user_id ON event_attendance(user_id);
CREATE INDEX idx_attendance_status ON event_attendance(status);



-- 6. EVENT REMINDERS TABLE

CREATE TABLE event_reminders (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    reminder_time TIMESTAMP NOT NULL,
    type VARCHAR(50) DEFAULT 'pre-event',
    sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reminders_event_id ON event_reminders(event_id);
CREATE INDEX idx_reminders_user_id ON event_reminders(user_id);
CREATE INDEX idx_reminders_time ON event_reminders(reminder_time);
CREATE INDEX idx_reminders_sent ON event_reminders(sent);



-- 7. CYBER FACTS TABLE

CREATE TABLE cyber_facts (
    id BIGSERIAL PRIMARY KEY,
    fact TEXT NOT NULL,
    category VARCHAR(100),
    added_by BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    approved BOOLEAN DEFAULT FALSE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    approved_by BIGINT REFERENCES admins(id) ON DELETE SET NULL
);

CREATE INDEX idx_facts_category ON cyber_facts(category);
CREATE INDEX idx_facts_approved ON cyber_facts(approved);
CREATE INDEX idx_facts_added_by ON cyber_facts(added_by);



-- 8. COMMANDS LOG TABLE

CREATE TABLE commands_log (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    command_name VARCHAR(255) NOT NULL,
    parameters TEXT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_commands_user_id ON commands_log(user_id);
CREATE INDEX idx_commands_name ON commands_log(command_name);
CREATE INDEX idx_commands_used_at ON commands_log(used_at);



-- 10. REACTIONS TABLE

CREATE TABLE reactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reaction VARCHAR(100) NOT NULL,
    reacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id,reaction)
);

CREATE INDEX idx_reactions_user_id ON reactions(user_id);
CREATE INDEX idx_reactions_reacted_at ON reactions(reacted_at);


-- 11. ANNOUNCEMENTS TABLE

CREATE TABLE announcements (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    sent_by BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_pinned BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_announcements_sent_by ON announcements(sent_by);
CREATE INDEX idx_announcements_sent_at ON announcements(sent_at);
CREATE INDEX idx_announcements_pinned ON announcements(is_pinned);



-- 12. DASHBOARD ACTIONS TABLE

CREATE TABLE dashboard_actions (
    id BIGSERIAL PRIMARY KEY,
    admin_id BIGINT NOT NULL REFERENCES admins(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    target_table VARCHAR(100),
    target_id BIGINT,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    details JSONB
);

CREATE INDEX idx_dashboard_admin_id ON dashboard_actions(admin_id);
CREATE INDEX idx_dashboard_action ON dashboard_actions(action);
CREATE INDEX idx_dashboard_time ON dashboard_actions(action_time);



-- VIEW: Upcoming Events
-- Shows only future events
CREATE VIEW upcoming_events AS
SELECT
    e.*,
    u.username as creator_username,
    COUNT(DISTINCT ea.user_id) as confirmed_attendees
FROM events e
JOIN users u ON e.created_by = u.id
LEFT JOIN event_attendance ea ON e.id = ea.event_id AND ea.status = 'attending'
WHERE e.event_date >= CURRENT_TIMESTAMP
    AND e.status = 'upcoming'
GROUP BY e.id, u.username
ORDER BY e.event_date ASC;



-- VIEW: Command Statistics
-- Shows command usage statistics
CREATE VIEW command_statistics AS
SELECT
    command_name,
    COUNT(*) as total_uses,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(CASE WHEN success = TRUE THEN 1 END) as successful_uses,
    COUNT(CASE WHEN success = FALSE THEN 1 END) as failed_uses,
    MAX(used_at) as last_used
FROM commands_log
GROUP BY command_name
ORDER BY total_uses DESC;



-- Trigger: Update events.updated_at on modification
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_events_modtime
    BEFORE UPDATE ON events
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Trigger 2: Log when admin performs actions
CREATE OR REPLACE FUNCTION log_admin_action()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO dashboard_actions (admin_id, action, target_table, target_id)
        SELECT a.id, 'CREATE', TG_TABLE_NAME, NEW.id
        FROM admins a
        WHERE a.user_id = NEW.created_by
        LIMIT 1;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO dashboard_actions (admin_id, action, target_table, target_id)
        SELECT a.id, 'UPDATE', TG_TABLE_NAME, NEW.id
        FROM admins a
        WHERE a.user_id = NEW.created_by
        LIMIT 1;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
