-- Enable pgcrypto extension for hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. Create Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index for email to speed up queries
CREATE INDEX idx_users_email ON users(email);

-- 2. Create Applications Table
CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    applied_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- : Add index for status in applications
CREATE INDEX idx_applications_status ON applications(status);

-- 3. Create Reminders Table
CREATE TABLE reminders (
    reminder_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    application_id INT,
    reminder_date TIMESTAMP NOT NULL,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE
);

-- 4. Create AI Insights Table
CREATE TABLE ai_insights (
    insight_id SERIAL PRIMARY KEY,
    application_id INT NOT NULL,
    trend_analysis TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE
);

-- 5. Create Teams Table
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index for team_name to speed up queries
CREATE INDEX idx_teams_team_name ON teams(team_name);

-- 6. Create Team Members Table
CREATE TABLE team_members (
    team_member_id SERIAL PRIMARY KEY,
    team_id INT NOT NULL,
    user_id INT NOT NULL,
    role VARCHAR(50) DEFAULT 'Member',
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 7. Insert Example Data with Password Hashing
INSERT INTO users (username, email, password_hash)
VALUES ('john_doe', 'john@example.com', crypt('password123', gen_salt('bf')));

-- 8. Verify Indexes (optional for debugging)
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'users' OR tablename = 'teams';

-- 9. Verify Password Hashes (optional for debugging)
SELECT username, password_hash FROM users;
