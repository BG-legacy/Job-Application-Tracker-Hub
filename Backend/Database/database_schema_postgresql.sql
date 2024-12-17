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
DROP TABLE IF EXISTS applications CASCADE;
DROP TABLE IF EXISTS applications_application CASCADE;

CREATE TABLE applications_application (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    position VARCHAR(200) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    job_description TEXT,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'Pending' NOT NULL,
    applied_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Add indexes
CREATE INDEX idx_applications_status ON applications_application(status);
CREATE INDEX idx_applications_user ON applications_application(user_id);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_applications_updated_at
    BEFORE UPDATE ON applications_application
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

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

-- Rename columns to match our schema
ALTER TABLE applications_application 
    RENAME COLUMN company TO company_name;

ALTER TABLE applications_application 
    RENAME COLUMN date_applied TO applied_date;

-- Add missing column
ALTER TABLE applications_application 
    ADD COLUMN job_title VARCHAR(255);

-- Update column types and constraints
ALTER TABLE applications_application 
    ALTER COLUMN company_name TYPE VARCHAR(255),
    ALTER COLUMN status TYPE VARCHAR(20),
    ALTER COLUMN status SET DEFAULT 'Pending';

-- Update existing job_title values (if needed)
UPDATE applications_application 
SET job_title = 'Not Specified' 
WHERE job_title IS NULL;

-- Add NOT NULL constraint to job_title after setting default value
ALTER TABLE applications_application 
    ALTER COLUMN job_title SET NOT NULL;

-- Verify changes
\d applications_application
