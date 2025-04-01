DROP DATABASE IF EXISTS uplift;
CREATE DATABASE IF NOT EXISTS uplift;
USE uplift;

DROP TABLE IF EXISTS feedback_forms;
DROP TABLE IF EXISTS organization_locations;
DROP TABLE IF EXISTS program_locations;
DROP TABLE IF EXISTS program_categories;
DROP TABLE IF EXISTS organization_categories;
DROP TABLE IF EXISTS user_programs;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS point_of_contacts;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS qualifications;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS user_profiles;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    type ENUM('admin', 'user', 'data_analyst', 'organization_admin') NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_name (first_name, last_name),
    INDEX idx_user_type (type)
);

CREATE TABLE user_profiles (
    user_id CHAR(36) NOT NULL PRIMARY KEY,
    date_of_birth DATE,
    gender VARCHAR(20),
    income INT,
    education_level VARCHAR(50),
    employment_status VARCHAR(50),
    veteran_status BOOLEAN DEFAULT FALSE,
    disability_status BOOLEAN DEFAULT FALSE,
    ssn VARCHAR(11),
    verification_status ENUM('unverified', 'pending', 'verified') DEFAULT 'unverified',
    verification_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE organizations (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    website_url VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_organization_verified (is_verified)
);

CREATE TABLE categories (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(50) NOT NULL UNIQUE,
    INDEX idx_category_name (name)
);

CREATE TABLE programs (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status ENUM('open', 'close') NOT NULL DEFAULT 'open',
    start_date DATE,
    deadline TIMESTAMP,
    end_date DATE,
    organization_id CHAR(36) NOT NULL,
    category_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_program_status (status),
    INDEX idx_program_deadline (deadline),
    INDEX idx_program_category (category_id),
    INDEX idx_program_organization (organization_id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE qualifications (
    program_id CHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    qualification_type ENUM('income', 'age', 'family_size', 'location', 'education', 'disability', 'veteran_status', 'citizenship', 'other') NOT NULL,
    min_value DECIMAL(10,2),
    max_value DECIMAL(10,2),
    text_value VARCHAR(255),
    boolean_value BOOLEAN,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE,
    INDEX idx_qualification_program (program_id),
    INDEX idx_qualification_type (qualification_type)
);

CREATE TABLE applications (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    program_id CHAR(36) NOT NULL,
    status ENUM('draft', 'submitted', 'under_review', 'additional_info_needed', 'approved', 'rejected', 'waitlisted', 'withdrawn') NOT NULL DEFAULT 'draft',
    qualification_status ENUM('pending', 'verified', 'incomplete', 'rejected') DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decision_date TIMESTAMP,
    decision_notes TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_application_user (user_id),
    INDEX idx_application_program (program_id),
    INDEX idx_application_date (applied_at),
    INDEX idx_application_status (status),
    INDEX idx_application_qual_status (qualification_status),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE,
    UNIQUE KEY unq_user_program (user_id, program_id)
);

CREATE TABLE point_of_contacts (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    contact_type ENUM('user', 'organization') NOT NULL,
    entity_id CHAR(36) NOT NULL,
    description VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_contact_type (contact_type),
    INDEX idx_contact_entity (entity_id)
);

CREATE TABLE feedback_forms (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    program_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_feedback_program (program_id),
    INDEX idx_feedback_user (user_id),
    effectiveness INT NOT NULL,
    experience INT NOT NULL,
    simplicity INT NOT NULL,
    recommendation INT NOT NULL,
    improvement text NOT NULL,
    CHECK (effectiveness >= 0 AND effectiveness <= 5),
    CHECK (experience >= 0 AND experience <= 5),
    CHECK (simplicity >= 0 AND simplicity <= 5),
    CHECK (recommendation >= 0 AND recommendation <= 5),
    UNIQUE KEY unq_user_feedback_program (user_id, program_id)
);

CREATE TABLE locations (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    location_type ENUM('user', 'program', 'organization') NOT NULL,
    entity_id CHAR(36) NOT NULL,
    type ENUM('virtual', 'physical') NOT NULL,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    country VARCHAR(100) DEFAULT 'United States',
    is_primary BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_location_entity (location_type, entity_id),
    INDEX idx_location_state (state),
    INDEX idx_location_city (city),
    INDEX idx_location_zip (zip_code),
    INDEX idx_location_primary (is_primary)
);

CREATE TABLE user_programs (
    user_id CHAR(36) NOT NULL,
    program_id CHAR(36) NOT NULL,
    PRIMARY KEY (user_id, program_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
);

CREATE TABLE organization_categories (
    organization_id CHAR(36) NOT NULL,
    category_id CHAR(36) NOT NULL,
    PRIMARY KEY (organization_id, category_id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_org_category (organization_id, category_id)
);

CREATE TABLE program_categories (
    program_id CHAR(36) NOT NULL,
    category_id CHAR(36) NOT NULL,
    PRIMARY KEY (program_id, category_id),
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_program_category (program_id, category_id)
);

CREATE TABLE program_locations (
    program_id CHAR(36) NOT NULL,
    location_id CHAR(36) NOT NULL,
    PRIMARY KEY (program_id, location_id),
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_program_location (program_id, location_id)
);

CREATE TABLE organization_locations (
    organization_id CHAR(36) NOT NULL,
    location_id CHAR(36) NOT NULL,
    PRIMARY KEY (organization_id, location_id),
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    INDEX idx_organization_location (organization_id, location_id)
);



INSERT INTO users VALUES
('11111111-1111-1111-1111-111111111111', 'John', 'Doe', 'admin', '2024-01-01 10:00:00'),
('22222222-2222-2222-2222-222222222222', 'Jane', 'Smith', 'user', '2024-01-02 11:00:00'),
('33333333-3333-3333-3333-333333333333', 'Robert', 'Johnson', 'data_analyst', '2024-01-03 12:00:00'),
('44444444-4444-4444-4444-444444444444', 'Sarah', 'Williams', 'organization_admin', '2024-01-04 13:00:00'),
('55555555-5555-5555-5555-555555555555', 'Michael', 'Brown', 'user', '2024-01-05 14:00:00');

INSERT INTO user_profiles VALUES
('11111111-1111-1111-1111-111111111111', '1980-06-15', 'Male', 75000, 'Masters', 'Employed', FALSE, FALSE, NULL, 'verified', '2024-01-10 10:30:00', '2024-01-10 10:30:00'),
('22222222-2222-2222-2222-222222222222', '1992-03-20', 'Female', 45000, 'Bachelors', 'Employed', FALSE, FALSE, NULL, 'verified', '2024-01-12 11:15:00', '2024-01-12 11:15:00'),
('33333333-3333-3333-3333-333333333333', '1985-11-08', 'Male', 85000, 'PhD', 'Employed', TRUE, FALSE, NULL, 'verified', '2024-01-14 09:45:00', '2024-01-14 09:45:00'),
('44444444-4444-4444-4444-444444444444', '1990-09-25', 'Female', 65000, 'Masters', 'Employed', FALSE, FALSE, NULL, 'verified', '2024-01-15 13:20:00', '2024-01-15 13:20:00'),
('55555555-5555-5555-5555-555555555555', '1995-04-12', 'Male', 35000, 'High School', 'Part-time', FALSE, TRUE, NULL, 'pending', NULL, '2024-01-16 15:10:00');

INSERT INTO organizations VALUES
('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'Community Support Foundation', 'Non-profit focused on community welfare programs', 'https://csf.org', TRUE, '2024-01-05 10:30:00', '2024-01-01 09:00:00', '2024-01-01 09:00:00'),
('BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB', 'Education Advancement Initiative', 'Promoting educational opportunities for underserved communities', 'https://eai.org', TRUE, '2024-01-06 14:20:00', '2024-01-02 10:00:00', '2024-01-02 10:00:00'),
('CCCCCCCC-CCCC-CCCC-CCCC-CCCCCCCCCCCC', 'Housing Assistance Network', 'Providing housing support and homelessness prevention', 'https://han.org', TRUE, '2024-01-07 11:45:00', '2024-01-03 11:00:00', '2024-01-03 11:00:00'),
('DDDDDDDD-DDDD-DDDD-DDDD-DDDDDDDDDDDD', 'Veterans Support Services', 'Assisting veterans with reintegration and support', 'https://vss.org', FALSE, NULL, '2024-01-04 12:00:00', '2024-01-04 12:00:00'),
('EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE', 'Healthcare Access Program', 'Expanding healthcare access to underserved populations', 'https://hap.org', FALSE, NULL, '2024-01-05 13:00:00', '2024-01-05 13:00:00');

INSERT INTO categories VALUES
('FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF', 'Financial Assistance'),
('GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG', 'Education'),
('HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH', 'Housing'),
('IIIIIIII-IIII-IIII-IIII-IIIIIIIIIIII', 'Healthcare'),
('JJJJJJJJ-JJJJ-JJJJ-JJJJ-JJJJJJJJJJJJ', 'Employment'),
('KKKKKKKK-KKKK-KKKK-KKKK-KKKKKKKKKKKK', 'Veterans');

INSERT INTO programs VALUES
('LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'Emergency Rental Assistance', 'Financial support for rent payments during emergencies', 'open', '2024-01-15', '2024-07-15 23:59:59', '2024-12-31', 'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH', '2024-01-10 09:00:00', '2024-01-10 09:00:00'),
('MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'Scholarship Program', 'Educational scholarships for low-income students', 'open', '2024-02-01', '2024-05-30 23:59:59', '2025-06-30', 'BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB', 'GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG', '2024-01-11 10:00:00', '2024-01-11 10:00:00'),
('NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN', 'Veteran Job Training', 'Employment training for veterans', 'open', '2024-03-01', '2024-08-31 23:59:59', '2024-12-15', 'DDDDDDDD-DDDD-DDDD-DDDD-DDDDDDDDDDDD', 'KKKKKKKK-KKKK-KKKK-KKKK-KKKKKKKKKKKK', '2024-01-12 11:00:00', '2024-01-12 11:00:00'),
('OOOOOOOO-OOOO-OOOO-OOOO-OOOOOOOOOOOO', 'Healthcare Subsidy', 'Subsidies for medical care for low-income individuals', 'open', '2024-01-20', '2024-12-31 23:59:59', '2025-12-31', 'EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE', 'IIIIIIII-IIII-IIII-IIII-IIIIIIIIIIII', '2024-01-13 12:00:00', '2024-01-13 12:00:00'),
('PPPPPPPP-PPPP-PPPP-PPPP-PPPPPPPPPPPP', 'Job Placement Assistance', 'Employment placement services', 'close', '2023-07-01', '2023-12-31 23:59:59', '2024-01-31', 'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'JJJJJJJJ-JJJJ-JJJJ-JJJJ-JJJJJJJJJJJJ', '2023-06-15 13:00:00', '2024-02-01 09:00:00');

INSERT INTO qualifications (program_id, name, description, qualification_type, min_value, max_value, text_value, boolean_value) VALUES
('LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'Income Limit', 'Maximum household income to qualify', 'income', 0, 50000, NULL, NULL),
('LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'Residency', 'Must be a resident of eligible counties', 'location', NULL, NULL, 'County residency required', NULL),
('MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'Age Requirement', 'Age range for scholarship eligibility', 'age', 16, 25, NULL, NULL),
('MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'GPA Minimum', 'Minimum GPA requirement', 'education', 3.0, NULL, NULL, NULL),
('NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN', 'Veteran Status', 'Must be a veteran', 'veteran_status', NULL, NULL, NULL, TRUE),
('OOOOOOOO-OOOO-OOOO-OOOO-OOOOOOOOOOOO', 'Income Threshold', 'Income must be below federal poverty level', 'income', 0, 30000, NULL, NULL),
('PPPPPPPP-PPPP-PPPP-PPPP-PPPPPPPPPPPP', 'Unemployment', 'Must be currently unemployed', 'other', NULL, NULL, NULL, TRUE);

INSERT INTO applications VALUES
('QQQQQQQQ-QQQQ-QQQQ-QQQQ-QQQQQQQQQQQQ', '22222222-2222-2222-2222-222222222222', 'LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'submitted', 'pending', '2024-01-20 14:30:00', NULL, NULL, '2024-01-20 14:30:00'),
('RRRRRRRR-RRRR-RRRR-RRRR-RRRRRRRRRRRR', '55555555-5555-5555-5555-555555555555', 'MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'under_review', 'verified', '2024-02-05 10:15:00', NULL, NULL, '2024-02-07 13:20:00'),
('SSSSSSSS-SSSS-SSSS-SSSS-SSSSSSSSSSSS', '33333333-3333-3333-3333-333333333333', 'NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN', 'approved', 'verified', '2024-03-10 09:45:00', '2024-03-15 11:30:00', 'Approved based on service record and qualifications', '2024-03-15 11:30:00'),
('TTTTTTTT-TTTT-TTTT-TTTT-TTTTTTTTTTTT', '22222222-2222-2222-2222-222222222222', 'OOOOOOOO-OOOO-OOOO-OOOO-OOOOOOOOOOOO', 'rejected', 'rejected', '2024-02-12 15:20:00', '2024-02-18 10:00:00', 'Income exceeds program threshold', '2024-02-18 10:00:00'),
('UUUUUUUU-UUUU-UUUU-UUUU-UUUUUUUUUUUU', '55555555-5555-5555-5555-555555555555', 'PPPPPPPP-PPPP-PPPP-PPPP-PPPPPPPPPPPP', 'draft', 'pending', '2024-01-18 16:40:00', NULL, NULL, '2024-01-18 16:40:00');

INSERT INTO point_of_contacts VALUES
('VVVVVVVV-VVVV-VVVV-VVVV-VVVVVVVVVVVV', 'organization', 'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'Program Director', 'director@csf.org', '555-123-4567', '2024-01-05 10:00:00', '2024-01-05 10:00:00'),
('WWWWWWWW-WWWW-WWWW-WWWW-WWWWWWWWWWWW', 'organization', 'BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB', 'Scholarship Coordinator', 'scholarships@eai.org', '555-234-5678', '2024-01-06 11:00:00', '2024-01-06 11:00:00'),
('XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', 'organization', 'CCCCCCCC-CCCC-CCCC-CCCC-CCCCCCCCCCCC', 'Housing Director', 'housing@han.org', '555-345-6789', '2024-01-07 12:00:00', '2024-01-07 12:00:00'),
('YYYYYYYY-YYYY-YYYY-YYYY-YYYYYYYYYYYY', 'user', '22222222-2222-2222-2222-222222222222', 'Applicant', 'jane.smith@email.com', '555-456-7890', '2024-01-10 14:00:00', '2024-01-10 14:00:00'),
('ZZZZZZZZ-ZZZZ-ZZZZ-ZZZZ-ZZZZZZZZZZZZ', 'user', '33333333-3333-3333-3333-333333333333', 'Veteran Support Contact', 'robert.johnson@email.com', '555-567-8901', '2024-01-11 15:00:00', '2024-01-11 15:00:00');

INSERT INTO feedback_forms VALUES
('111111AA-AAAA-AAAA-AAAA-111111AAAAAA', 'LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', '11111111-1111-1111-1111-111111111111', 'Feedback Form 1', '2024-01-15 10:00:00', '2024-01-20 07:00:00', 1, 2, 3, 4, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur malesuada nunc viverra nunc consectetur, non consectetur metus vehicula.'),
('222222BB-BBBB-BBBB-BBBB-222222BBBBBB', 'MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', '22222222-2222-2222-2222-222222222222', 'Feedback Form 2', '2022-09-28 02:30:00', '2023-08-31 11:45:00', 5, 4, 3, 2, 'Integer scelerisque faucibus ex a maximus. Integer scelerisque vulputate dui, in placerat ante lacinia in. Nullam at mi in urna laoreet ullamcorper et non nibh. Etiam sed massa sed turpis gravida ullamcorper ac sit amet magna.'),
('333333CC-CCCC-CCCC-CCCC-333333CCCCCC', 'NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN', '33333333-3333-3333-3333-333333333333', 'Feedback Form 3', '2017-03-17 04:02:52', '2025-12-12 12:57:11', 3, 3, 3, 3, 'Integer vulputate dui, placerat lacinia in. Nullam at mi in urna laoreetsed massa sed turpis gravida ullamcorper ac sit amet magna.'),
('444444DD-DDDD-DDDD-DDDD-444444DDDDDD', 'OOOOOOOO-OOOO-OOOO-OOOO-OOOOOOOOOOOO', '44444444-4444-4444-4444-444444444444', 'Feedback Form 4', '2019-11-01 05:53:22', '2020-05-07 09:21:44', 4, 4, 4, 4, 'Etiam ut posuere nisl, ac tristique nibh. In hac habitasse platea dictumst. Nulla a nunc eleifend, eleifend nunc sed, pellentesque ex.');

INSERT INTO locations VALUES
('777777GG-GGGG-GGGG-GGGG-777777GGGGGG', 'organization', 'AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'physical', '123 Main Street', 'Suite 100', 'Chicago', 'Illinois', '60601', 'United States', TRUE, '2024-01-05 10:30:00', '2024-01-05 10:30:00'),
('888888HH-HHHH-HHHH-HHHH-888888HHHHHH', 'organization', 'BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB', 'physical', '456 Oak Avenue', 'Building B', 'Atlanta', 'Georgia', '30301', 'United States', TRUE, '2024-01-06 11:30:00', '2024-01-06 11:30:00'),
('999999II-IIII-IIII-IIII-999999IIIIII', 'program', 'LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'physical', '123 Main Street', 'Suite 101', 'Chicago', 'Illinois', '60601', 'United States', TRUE, '2024-01-10 09:30:00', '2024-01-10 09:30:00'),
('AAAAAA11-1111-1111-1111-AAAAAA111111', 'program', 'MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'virtual', NULL, NULL, 'Online', 'N/A', '00000', 'United States', TRUE, '2024-01-11 10:30:00', '2024-01-11 10:30:00'),
('BBBBBB22-2222-2222-2222-BBBBBB222222', 'user', '22222222-2222-2222-2222-222222222222', 'physical', '789 Elm Street', 'Apt 304', 'Denver', 'Colorado', '80201', 'United States', TRUE, '2024-01-10 14:30:00', '2024-01-10 14:30:00');

INSERT INTO user_programs VALUES
('22222222-2222-2222-2222-222222222222', 'LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL'),
('33333333-3333-3333-3333-333333333333', 'NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN'),
('55555555-5555-5555-5555-555555555555', 'MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM');

INSERT INTO organization_categories VALUES
('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'),
('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH'),
('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', 'JJJJJJJJ-JJJJ-JJJJ-JJJJ-JJJJJJJJJJJJ'),
('BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB', 'GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG'),
('CCCCCCCC-CCCC-CCCC-CCCC-CCCCCCCCCCCC', 'HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH');

INSERT INTO program_categories VALUES
('LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH'),
('LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'),
('MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG'),
('NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN', 'KKKKKKKK-KKKK-KKKK-KKKK-KKKKKKKKKKKK'),
('NNNNNNNN-NNNN-NNNN-NNNN-NNNNNNNNNNNN', 'JJJJJJJJ-JJJJ-JJJJ-JJJJ-JJJJJJJJJJJJ'),
('OOOOOOOO-OOOO-OOOO-OOOO-OOOOOOOOOOOO', 'IIIIIIII-IIII-IIII-IIII-IIIIIIIIIIII');

INSERT INTO program_locations VALUES
('LLLLLLLL-LLLL-LLLL-LLLL-LLLLLLLLLLLL', '999999II-IIII-IIII-IIII-999999IIIIII'),
('MMMMMMMM-MMMM-MMMM-MMMM-MMMMMMMMMMMM', 'AAAAAA11-1111-1111-1111-AAAAAA111111');

INSERT INTO organization_locations VALUES
('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA', '777777GG-GGGG-GGGG-GGGG-777777GGGGGG'),
('BBBBBBBB-BBBB-BBBB-BBBB-BBBBBBBBBBBB', '888888HH-HHHH-HHHH-HHHH-888888HHHHHH');


