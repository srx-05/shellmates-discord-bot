



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
-- Stores server administrators and bot managers
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

-- ==========================================


-- 3. PERMISSIONS TABLE
-- Defines admin permissions for each module
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

-- ==========================================

-- 4. EVENTS TABLE
-- Stores all events, workshops, and competitions
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

-- ==========================================

-- 5. EVENT ATTENDANCE TABLE
-- Tracks attendance status for each member per event
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

-- ==========================================

-- 6. EVENT REMINDERS TABLE
-- Stores reminders for events
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

-- ==========================================

-- 7. CYBER FACTS TABLE
-- Stores cybersecurity facts for educational purposes
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

-- ==========================================

-- 8. COMMANDS LOG TABLE
-- Logs all bot command usage
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
-- Tracks reactions on messages
CREATE TABLE reactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reaction VARCHAR(100) NOT NULL,
    reacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id,reaction)
);

CREATE INDEX idx_reactions_user_id ON reactions(user_id);
CREATE INDEX idx_reactions_reacted_at ON reactions(reacted_at);

-- ==========================================

-- 11. ANNOUNCEMENTS TABLE
-- Stores official announcements for all members
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

-- ==========================================

-- 12. DASHBOARD ACTIONS TABLE (Optional)
-- Logs admin actions on the web dashboard
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

-- ==========================================
-- VIEWS
-- ==========================================

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

-- ==========================================

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

-- ==========================================
-- TRIGGERS
-- ==========================================

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









-- ==========================================
-- الجزء 5: Stored Procedures (إجراءات مخزنة)
-- ==========================================

-- Procedure 1: إضافة مستخدم جديد
CREATE OR REPLACE FUNCTION add_user(
    p_discord_id VARCHAR(100),
    p_username VARCHAR(255)
) RETURNS BIGINT AS $$
DECLARE
    v_user_id BIGINT;
BEGIN
    INSERT INTO users (discord_id, username)
    VALUES (p_discord_id, p_username)
    ON CONFLICT (discord_id) DO UPDATE
    SET username = EXCLUDED.username
    RETURNING id INTO v_user_id;

    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;

-- Procedure 2: تسجيل حضور حدث
CREATE OR REPLACE FUNCTION register_event_attendance(
    p_event_id BIGINT,
    p_user_id BIGINT,
    p_status VARCHAR(50)
) RETURNS BOOLEAN AS $$
DECLARE
    v_max_participants INTEGER;
    v_current_count INTEGER;
BEGIN
    -- التحقق من العدد الأقصى
    SELECT max_participants INTO v_max_participants
    FROM events WHERE id = p_event_id;

    IF v_max_participants IS NOT NULL THEN
        SELECT COUNT(*) INTO v_current_count
        FROM event_attendance
        WHERE event_id = p_event_id AND status = 'attending';

        IF v_current_count >= v_max_participants AND p_status = 'attending' THEN
            RAISE EXCEPTION 'Event is full';
        END IF;
    END IF;

    -- تسجيل الحضور
    INSERT INTO event_attendance (event_id, user_id, status, responded_at)
    VALUES (p_event_id, p_user_id, p_status, CURRENT_TIMESTAMP)
    ON CONFLICT (event_id, user_id)
    DO UPDATE SET status = EXCLUDED.status, responded_at = CURRENT_TIMESTAMP;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Procedure 3: إنشاء حدث مع تذكيرات تلقائية
CREATE OR REPLACE FUNCTION create_event_with_reminders(
    p_title VARCHAR(255),
    p_description TEXT,
    p_event_date TIMESTAMP,
    p_location VARCHAR(255),
    p_created_by BIGINT
) RETURNS BIGINT AS $$
DECLARE
    v_event_id BIGINT;
BEGIN
    -- إنشاء الحدث
    INSERT INTO events (title, description, event_date, location, created_by)
    VALUES (p_title, p_description, p_event_date, p_location, p_created_by)
    RETURNING id INTO v_event_id;

    -- إضافة تذكير قبل يوم
    INSERT INTO event_reminders (event_id, reminder_time, type)
    VALUES (v_event_id, p_event_date - INTERVAL '1 day', 'pre-event');

    -- إضافة تذكير قبل ساعة
    INSERT INTO event_reminders (event_id, reminder_time, type)
    VALUES (v_event_id, p_event_date - INTERVAL '1 hour', 'pre-event');

    -- إضافة تذكير عند البداية
    INSERT INTO event_reminders (event_id, reminder_time, type)
    VALUES (v_event_id, p_event_date, 'at-event');

    RETURN v_event_id;
END;
$$ LANGUAGE plpgsql;

-- Procedure 4: الحصول على إحصائيات المستخدم
CREATE OR REPLACE FUNCTION get_user_statistics(p_user_id BIGINT)
RETURNS TABLE (
    total_commands INTEGER,
    total_events_attended INTEGER,
    total_messages INTEGER,
    total_reactions INTEGER,
    total_facts_added INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(DISTINCT cl.id)::INTEGER,
        COUNT(DISTINCT ea.id)::INTEGER,
        COUNT(DISTINCT m.id)::INTEGER,
        COUNT(DISTINCT r.id)::INTEGER,
        COUNT(DISTINCT cf.id)::INTEGER
    FROM users u
    LEFT JOIN commands_log cl ON u.id = cl.user_id
    LEFT JOIN event_attendance ea ON u.id = ea.user_id
    LEFT JOIN messages m ON u.id = m.user_id
    LEFT JOIN reactions r ON u.id = r.user_id
    LEFT JOIN cyber_facts cf ON u.id = cf.added_by
    WHERE u.id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- الجزء 6: بيانات تجريبية (Sample Data)
-- ==========================================

-- إضافة مستخدمين تجريبيين
INSERT INTO users (discord_id, username) VALUES
('123456789012345678', 'Admin_User'),
('234567890123456789', 'Mohamed_Ahmed'),
('345678901234567890', 'Fatima_Ali'),
('456789012345678901', 'Omar_Hassan'),
('567890123456789012', 'Sara_Ibrahim');

-- إضافة مشرفين
INSERT INTO admins (user_id, role) VALUES
((SELECT id FROM users WHERE discord_id = '123456789012345678'), 'super_admin'),
((SELECT id FROM users WHERE discord_id = '234567890123456789'), 'moderator');

-- إضافة صلاحيات للمشرفين
INSERT INTO permissions (admin_id, module, can_create, can_read, can_update, can_delete) VALUES
(1, 'events', TRUE, TRUE, TRUE, TRUE),
(1, 'facts', TRUE, TRUE, TRUE, TRUE),
(1, 'announcements', TRUE, TRUE, TRUE, TRUE),
(2, 'events', TRUE, TRUE, TRUE, FALSE),
(2, 'facts', TRUE, TRUE, FALSE, FALSE);

-- إضافة أحداث تجريبية
INSERT INTO events (title, description, event_date, location, created_by, status) VALUES
('ورشة Python للمبتدئين', 'تعلم أساسيات البرمجة بلغة Python', NOW() + INTERVAL '7 days', 'Online - Discord Voice', 1, 'upcoming'),
('مسابقة CTF الشهرية', 'اختبر مهاراتك في الأمن السيبراني', NOW() + INTERVAL '14 days', 'Online Platform', 1, 'upcoming'),
('محاضرة Web Security', 'فهم ثغرات الويب الشائعة وكيفية حمايتها', NOW() + INTERVAL '3 days', 'Online - Discord Voice', 2, 'upcoming');

-- إضافة حقائق سيبرانية
INSERT INTO cyber_facts (fact, category, added_by, approved) VALUES
('يجب أن تحتوي كلمة المرور القوية على 12 حرفاً على الأقل مع مزيج من الأحرف والأرقام والرموز', 'passwords', 1, TRUE),
('التصيد الاحتيالي (Phishing) هو أحد أكثر الهجمات السيبرانية شيوعاً', 'security', 1, TRUE),
('المصادقة الثنائية (2FA) تزيد من أمان حسابك بنسبة 99.9%', 'authentication', 2, TRUE);

-- ==========================================
-- الجزء 7: استعلامات مفيدة للإدارة
-- ==========================================

-- 1. عرض كل الأحداث القادمة مع عدد المشاركين
SELECT
    e.id,
    e.title,
    e.event_date,
    e.status,
    COUNT(ea.user_id) FILTER (WHERE ea.status = 'attending') as confirmed,
    COUNT(ea.user_id) FILTER (WHERE ea.status = 'pending') as pending
FROM events e
LEFT JOIN event_attendance ea ON e.id = ea.event_id
WHERE e.event_date >= CURRENT_TIMESTAMP
GROUP BY e.id
ORDER BY e.event_date;

-- 2. عرض أكثر الأوامر استخداماً
SELECT
    command_name,
    COUNT(*) as usage_count,
    COUNT(DISTINCT user_id) as unique_users
FROM commands_log
WHERE used_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY command_name
ORDER BY usage_count DESC
LIMIT 10;

-- 3. عرض المستخدمين الأكثر نشاطاً
SELECT
    u.username,
    COUNT(DISTINCT cl.id) as commands_used,
    COUNT(DISTINCT ea.id) as events_attended,
    COUNT(DISTINCT m.id) as messages_sent
FROM users u
LEFT JOIN commands_log cl ON u.id = cl.user_id
LEFT JOIN event_attendance ea ON u.id = ea.user_id
LEFT JOIN messages m ON u.id = m.user_id
GROUP BY u.id, u.username
ORDER BY commands_used DESC
LIMIT 10;

-- 4. عرض الحقائق التي تحتاج موافقة
SELECT
    cf.id,
    cf.fact,
    cf.category,
    u.username as added_by_user,
    cf.added_at
FROM cyber_facts cf
JOIN users u ON cf.added_by = u.id
WHERE cf.approved = FALSE
ORDER BY cf.added_at DESC;

-- ==========================================
-- الجزء 8: Backup و Maintenance
-- ==========================================

-- Script للنسخ الاحتياطي (تشغيله من Terminal)
-- pg_dump -U discord_bot_user -d discord_bot_db -F c -b -v -f backup_$(date +%Y%m%d).backup

-- تنظيف السجلات القديمة (أكثر من 90 يوم)
CREATE OR REPLACE FUNCTION cleanup_old_logs()
RETURNS void AS $$
BEGIN
    DELETE FROM commands_log WHERE used_at < CURRENT_DATE - INTERVAL '90 days';
    DELETE FROM dashboard_actions WHERE action_time < CURRENT_DATE - INTERVAL '90 days';
    DELETE FROM event_reminders WHERE sent = TRUE AND reminder_time < CURRENT_DATE - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- جدولة التنظيف التلقائي (يمكن استخدام pg_cron)
-- SELECT cron.schedule('cleanup-old-logs', '0 2 * * 0', 'SELECT cleanup_old_logs()');

-- ==========================================
-- الجزء 9: منح الصلاحيات النهائية
-- ==========================================

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO discord_bot_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO discord_bot_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO discord_bot_user;
