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
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
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
    ssn VARCHAR(11) NOT NULL,
    verification_status ENUM('unverified', 'pending', 'verified') DEFAULT 'unverified',
    verification_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE organizations (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
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
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
    name VARCHAR(50) NOT NULL UNIQUE,
    INDEX idx_category_name (name)
);

CREATE TABLE programs (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
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
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
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
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
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
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
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
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()) NOT NULL,
    location_type ENUM('user', 'program', 'organization') NOT NULL,
    entity_id CHAR(36) NOT NULL,
    type ENUM('virtual', 'physical') NOT NULL,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    country VARCHAR(100) DEFAULT 'United States' NOT NULL,
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
('831a22c1-5728-4691-b4ff-7b2c010f8b56', 'John', 'Doe', 'admin', '2024-01-01 10:00:00'),
('7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'Jane', 'Smith', 'user', '2024-01-02 11:00:00'),
('cd28292a-eadd-42ee-8cef-3397a8bb353a', 'Robert', 'Johnson', 'data_analyst', '2024-01-03 12:00:00'),
('a0ec60c0-28ce-475e-be6a-ac4bbdb44ada', 'Sarah', 'Williams', 'organization_admin', '2024-01-04 13:00:00'),
('f78d3b42-3965-40d6-98e0-f02c8ef76ba1', 'Michael', 'Brown', 'user', '2024-01-05 14:00:00');

INSERT INTO user_profiles VALUES
('831a22c1-5728-4691-b4ff-7b2c010f8b56', '1980-06-15', 'Male', 75000, 'Masters', 'Employed', FALSE, FALSE, 12345, 'verified', '2024-01-10 10:30:00', '2024-01-10 10:30:00'),
('7e9df825-1e91-4ed0-86c9-8b1f786edcce', '1992-03-20', 'Female', 45000, 'Bachelors', 'Employed', FALSE, FALSE, 23456, 'verified', '2024-01-12 11:15:00', '2024-01-12 11:15:00'),
('cd28292a-eadd-42ee-8cef-3397a8bb353a', '1985-11-08', 'Male', 85000, 'PhD', 'Employed', TRUE, FALSE, 34567, 'verified', '2024-01-14 09:45:00', '2024-01-14 09:45:00'),
('a0ec60c0-28ce-475e-be6a-ac4bbdb44ada', '1990-09-25', 'Female', 65000, 'Masters', 'Employed', FALSE, FALSE, 45678, 'verified', '2024-01-15 13:20:00', '2024-01-15 13:20:00'),
('f78d3b42-3965-40d6-98e0-f02c8ef76ba1', '1995-04-12', 'Male', 35000, 'High School', 'Part-time', FALSE, TRUE, 56789, 'pending', NULL, '2024-01-16 15:10:00');

INSERT INTO organizations VALUES
('b2f4a96d-9618-4f5f-8687-0519b20fbb4c', 'Community Support Foundation', 'Non-profit focused on community welfare programs', 'https://csf.org', TRUE, '2024-01-05 10:30:00', '2024-01-01 09:00:00', '2024-01-01 09:00:00'),
('5c17cb90-6c3f-47f3-9893-8d00c75a8bb4', 'Education Advancement Initiative', 'Promoting educational opportunities for underserved communities', 'https://eai.org', TRUE, '2024-01-06 14:20:00', '2024-01-02 10:00:00', '2024-01-02 10:00:00'),
('e3f089d1-6d8c-4876-b5cb-fe302c36aa47', 'Housing Assistance Network', 'Providing housing support and homelessness prevention', 'https://han.org', TRUE, '2024-01-07 11:45:00', '2024-01-03 11:00:00', '2024-01-03 11:00:00'),
('9f45b9c1-ae0a-4e5b-9b2d-cd6ba73e5c7d', 'Veterans Support Services', 'Assisting veterans with reintegration and support', 'https://vss.org', FALSE, NULL, '2024-01-04 12:00:00', '2024-01-04 12:00:00'),
('1d893f83-4e8c-4ecb-a3bd-1da5cb88057f', 'Healthcare Access Program', 'Expanding healthcare access to underserved populations', 'https://hap.org', FALSE, NULL, '2024-01-05 13:00:00', '2024-01-05 13:00:00');

INSERT INTO categories VALUES
('c782eb02-6391-4ee5-a5bf-58e91360de52', 'Financial Assistance'),
('2e345f0d-f984-4c1c-98a8-5c3d90ed71e4', 'Education'),
('78d6a9e8-6a19-40d0-9cc3-6a6bdf77586a', 'Housing'),
('4a1b45c9-7630-4e14-bdfa-d38d1301185b', 'Healthcare'),
('d7a9c5b2-8f6e-4d31-9b5e-942a3bfea897', 'Employment'),
('91c3f74d-6b4a-48e7-b3d2-5fa740e9c9d7', 'Veterans');

INSERT INTO programs VALUES
('f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', 'Emergency Rental Assistance', 'Financial support for rent payments during emergencies', 'open', '2024-01-15', '2024-07-15 23:59:59', '2024-12-31', 'b2f4a96d-9618-4f5f-8687-0519b20fbb4c', '78d6a9e8-6a19-40d0-9cc3-6a6bdf77586a', '2024-01-10 09:00:00', '2024-01-10 09:00:00'),
('e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', 'Scholarship Program', 'Educational scholarships for low-income students', 'open', '2024-02-01', '2024-05-30 23:59:59', '2025-06-30', '5c17cb90-6c3f-47f3-9893-8d00c75a8bb4', '2e345f0d-f984-4c1c-98a8-5c3d90ed71e4', '2024-01-11 10:00:00', '2024-01-11 10:00:00'),
('d1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3', 'Veteran Job Training', 'Employment training for veterans', 'open', '2024-03-01', '2024-08-31 23:59:59', '2024-12-15', '9f45b9c1-ae0a-4e5b-9b2d-cd6ba73e5c7d', '91c3f74d-6b4a-48e7-b3d2-5fa740e9c9d7', '2024-01-12 11:00:00', '2024-01-12 11:00:00'),
('c0926a5c-3b2a-39a5-62c8-95d0a7b8c3d2', 'Healthcare Subsidy', 'Subsidies for medical care for low-income individuals', 'open', '2024-01-20', '2024-12-31 23:59:59', '2025-12-31', '1d893f83-4e8c-4ecb-a3bd-1da5cb88057f', '4a1b45c9-7630-4e14-bdfa-d38d1301185b', '2024-01-13 12:00:00', '2024-01-13 12:00:00'),
('b9815a4b-2a19-28a4-51b7-84c9a6b7b2c1', 'Job Placement Assistance', 'Employment placement services', 'close', '2023-07-01', '2023-12-31 23:59:59', '2024-01-31', 'b2f4a96d-9618-4f5f-8687-0519b20fbb4c', 'd7a9c5b2-8f6e-4d31-9b5e-942a3bfea897', '2023-06-15 13:00:00', '2024-02-01 09:00:00');

INSERT INTO qualifications (program_id, name, description, qualification_type, min_value, max_value, text_value, boolean_value) VALUES
('f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', 'Income Limit', 'Maximum household income to qualify', 'income', 0, 50000, NULL, NULL),
('f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', 'Residency', 'Must be a resident of eligible counties', 'location', NULL, NULL, 'County residency required', NULL),
('e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', 'Age Requirement', 'Age range for scholarship eligibility', 'age', 16, 25, NULL, NULL),
('e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', 'GPA Minimum', 'Minimum GPA requirement', 'education', 3.0, NULL, NULL, NULL),
('d1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3', 'Veteran Status', 'Must be a veteran', 'veteran_status', NULL, NULL, NULL, TRUE),
('c0926a5c-3b2a-39a5-62c8-95d0a7b8c3d2', 'Income Threshold', 'Income must be below federal poverty level', 'income', 0, 30000, NULL, NULL),
('b9815a4b-2a19-28a4-51b7-84c9a6b7b2c1', 'Unemployment', 'Must be currently unemployed', 'other', NULL, NULL, NULL, TRUE);

INSERT INTO applications VALUES
('a8704a3a-1a08-17a3-40a6-73c8a5a6a1b0', '7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', 'submitted', 'pending', '2024-01-20 14:30:00', NULL, NULL, '2024-01-20 14:30:00'),
('97693929-0997-0692-39a5-62b7a4a5a0a9', 'f78d3b42-3965-40d6-98e0-f02c8ef76ba1', 'e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', 'under_review', 'verified', '2024-02-05 10:15:00', NULL, NULL, '2024-02-07 13:20:00'),
('86582818-9886-9581-28a4-51a6a3a4a9a8', 'cd28292a-eadd-42ee-8cef-3397a8bb353a', 'd1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3', 'approved', 'verified', '2024-03-10 09:45:00', '2024-03-15 11:30:00', 'Approved based on service record and qualifications', '2024-03-15 11:30:00'),
('75471707-8775-8470-17a3-40a5a2a3a8a7', '7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'c0926a5c-3b2a-39a5-62c8-95d0a7b8c3d2', 'rejected', 'rejected', '2024-02-12 15:20:00', '2024-02-18 10:00:00', 'Income exceeds program threshold', '2024-02-18 10:00:00'),
('64360696-7664-7369-0692-39a4a1a2a7a6', 'f78d3b42-3965-40d6-98e0-f02c8ef76ba1', 'b9815a4b-2a19-28a4-51b7-84c9a6b7b2c1', 'draft', 'pending', '2024-01-18 16:40:00', NULL, NULL, '2024-01-18 16:40:00');

INSERT INTO point_of_contacts VALUES
('53259585-6553-6258-9581-28a3a0a1a6a5', 'organization', 'b2f4a96d-9618-4f5f-8687-0519b20fbb4c', 'Program Director', 'director@csf.org', '555-123-4567', '2024-01-05 10:00:00', '2024-01-05 10:00:00'),
('42148474-5442-5147-8470-17a2a9a0a5a4', 'organization', '5c17cb90-6c3f-47f3-9893-8d00c75a8bb4', 'Scholarship Coordinator', 'scholarships@eai.org', '555-234-5678', '2024-01-06 11:00:00', '2024-01-06 11:00:00'),
('31037363-4331-4036-7369-06a1a8a9a4a3', 'organization', 'e3f089d1-6d8c-4876-b5cb-fe302c36aa47', 'Housing Director', 'housing@han.org', '555-345-6789', '2024-01-07 12:00:00', '2024-01-07 12:00:00'),
('20926252-3220-3925-6258-95a0a7a8a3a2', 'user', '7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'Applicant', 'jane.smith@email.com', '555-456-7890', '2024-01-10 14:00:00', '2024-01-10 14:00:00'),
('19815141-2119-2814-5147-84a9a6a7a2a1', 'user', 'cd28292a-eadd-42ee-8cef-3397a8bb353a', 'Veteran Support Contact', 'robert.johnson@email.com', '555-567-8901', '2024-01-11 15:00:00', '2024-01-11 15:00:00');

INSERT INTO feedback_forms VALUES
('08704030-1008-1703-4036-73a8a5a6a1a0', 'f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', '831a22c1-5728-4691-b4ff-7b2c010f8b56', 'Feedback Form 1', '2024-01-15 10:00:00', '2024-01-20 07:00:00', 1, 2, 3, 4, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur malesuada nunc viverra nunc consectetur, non consectetur metus vehicula.'),
('97693929-9997-9692-3925-62a7a4a5a0a9', 'e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', '7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'Feedback Form 2', '2022-09-28 02:30:00', '2023-08-31 11:45:00', 5, 4, 3, 2, 'Integer scelerisque faucibus ex a maximus. Integer scelerisque vulputate dui, in placerat ante lacinia in. Nullam at mi in urna laoreet ullamcorper et non nibh. Etiam sed massa sed turpis gravida ullamcorper ac sit amet magna.'),
('86582818-8886-8581-2814-51a6a3a4a9a8', 'd1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3', 'cd28292a-eadd-42ee-8cef-3397a8bb353a', 'Feedback Form 3', '2017-03-17 04:02:52', '2025-12-12 12:57:11', 3, 3, 3, 3, 'Integer vulputate dui, placerat lacinia in. Nullam at mi in urna laoreetsed massa sed turpis gravida ullamcorper ac sit amet magna.'),
('75471707-7775-7470-1703-40a5a2a3a8a7', 'c0926a5c-3b2a-39a5-62c8-95d0a7b8c3d2', 'a0ec60c0-28ce-475e-be6a-ac4bbdb44ada', 'Feedback Form 4', '2019-11-01 05:53:22', '2020-05-07 09:21:44', 4, 4, 4, 4, 'Etiam ut posuere nisl, ac tristique nibh. In hac habitasse platea dictumst. Nulla a nunc eleifend, eleifend nunc sed, pellentesque ex.');

INSERT INTO locations VALUES
('64360696-6664-6369-0692-39a4a1a2a7a6', 'organization', 'b2f4a96d-9618-4f5f-8687-0519b20fbb4c', 'physical', '123 Main Street', 'Suite 100', 'Chicago', 'Illinois', '60601', 'United States', TRUE, '2024-01-05 10:30:00', '2024-01-05 10:30:00'),
('53259585-5553-5258-9581-28a3a0a1a6a5', 'organization', '5c17cb90-6c3f-47f3-9893-8d00c75a8bb4', 'physical', '456 Oak Avenue', 'Building B', 'Atlanta', 'Georgia', '30301', 'United States', TRUE, '2024-01-06 11:30:00', '2024-01-06 11:30:00'),
('42148474-4442-4147-8470-17a2a9a0a5a4', 'program', 'f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', 'physical', '123 Main Street', 'Suite 101', 'Chicago', 'Illinois', '60601', 'United States', TRUE, '2024-01-10 09:30:00', '2024-01-10 09:30:00'),
('31037363-3331-3036-7369-06a1a8a9a4a3', 'program', 'e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', 'virtual', NULL, NULL, 'Online', 'N/A', '00000', 'United States', TRUE, '2024-01-11 10:30:00', '2024-01-11 10:30:00'),
('20926252-2220-2925-6258-95a0a7a8a3a2', 'user', '7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'physical', '789 Elm Street', 'Apt 304', 'Denver', 'Colorado', '80201', 'United States', TRUE, '2024-01-10 14:30:00', '2024-01-10 14:30:00');

INSERT INTO user_programs VALUES
('7e9df825-1e91-4ed0-86c9-8b1f786edcce', 'f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6'),
('cd28292a-eadd-42ee-8cef-3397a8bb353a', 'd1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3'),
('f78d3b42-3965-40d6-98e0-f02c8ef76ba1', 'e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4');

INSERT INTO organization_categories VALUES
('b2f4a96d-9618-4f5f-8687-0519b20fbb4c', 'c782eb02-6391-4ee5-a5bf-58e91360de52'),
('b2f4a96d-9618-4f5f-8687-0519b20fbb4c', '78d6a9e8-6a19-40d0-9cc3-6a6bdf77586a'),
('b2f4a96d-9618-4f5f-8687-0519b20fbb4c', 'd7a9c5b2-8f6e-4d31-9b5e-942a3bfea897'),
('5c17cb90-6c3f-47f3-9893-8d00c75a8bb4', '2e345f0d-f984-4c1c-98a8-5c3d90ed71e4'),
('e3f089d1-6d8c-4876-b5cb-fe302c36aa47', '78d6a9e8-6a19-40d0-9cc3-6a6bdf77586a');

INSERT INTO program_categories VALUES
('f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', '78d6a9e8-6a19-40d0-9cc3-6a6bdf77586a'),
('f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', 'c782eb02-6391-4ee5-a5bf-58e91360de52'),
('e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', '2e345f0d-f984-4c1c-98a8-5c3d90ed71e4'),
('d1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3', '91c3f74d-6b4a-48e7-b3d2-5fa740e9c9d7'),
('d1a37b6d-4c3d-40a6-73d9-a6e0b8c9d4e3', 'd7a9c5b2-8f6e-4d31-9b5e-942a3bfea897'),
('c0926a5c-3b2a-39a5-62c8-95d0a7b8c3d2', '4a1b45c9-7630-4e14-bdfa-d38d1301185b');

INSERT INTO program_locations VALUES
('f3a47d9c-6c5b-42a8-95e1-c8f2b1d8c5f6', '42148474-4442-4147-8470-17a2a9a0a5a4'),
('e2b48c7a-5d4e-41b7-84e0-b7f1c9d0a5e4', '31037363-3331-3036-7369-06a1a8a9a4a3');

INSERT INTO organization_locations VALUES
('b2f4a96d-9618-4f5f-8687-0519b20fbb4c', '64360696-6664-6369-0692-39a4a1a2a7a6'),
('5c17cb90-6c3f-47f3-9893-8d00c75a8bb4', '53259585-5553-5258-9581-28a3a0a1a6a5');