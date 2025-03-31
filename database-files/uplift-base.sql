DROP DATABASE IF EXISTS uplift;
CREATE DATABASE IF NOT EXISTS uplift;
USE uplift;

DROP TABLE IF EXISTS user_feedback_answers;
DROP TABLE IF EXISTS user_feedback_forms;
DROP TABLE IF EXISTS organization_locations;
DROP TABLE IF EXISTS program_locations;
DROP TABLE IF EXISTS program_categories;
DROP TABLE IF EXISTS organization_categories;
DROP TABLE IF EXISTS user_programs;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS feedback_questions;
DROP TABLE IF EXISTS feedback_forms;
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
    verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_organization_verified (verified)
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
    organization_id CHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    expiration_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE,
    INDEX idx_feedback_organization (organization_id),
    INDEX idx_feedback_active (active)
);

CREATE TABLE feedback_questions (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    feedback_form_id CHAR(36) NOT NULL,
    question VARCHAR(255) NOT NULL,
    question_type TEXT,
    options TEXT,
    question_order INT DEFAULT 0,
    rating_scale INT DEFAULT 5,
    required BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE,
    INDEX idx_question_form (feedback_form_id),
    UNIQUE KEY unq_question_order (feedback_form_id, question_order)
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

CREATE TABLE user_feedback_forms (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    user_id CHAR(36) NOT NULL,
    feedback_form_id CHAR(36) NOT NULL,
    status ENUM('in_progress', 'submitted') NOT NULL DEFAULT 'in_progress',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (feedback_form_id) REFERENCES feedback_forms(id) ON DELETE CASCADE,
    INDEX idx_feedback_user (user_id),
    INDEX idx_feedback_form (feedback_form_id)
);

CREATE TABLE user_feedback_answers (
    id CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID()),
    user_feedback_form_id CHAR(36) NOT NULL,
    question_id CHAR(36) NOT NULL,
    answer TEXT,
    rating INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_feedback_form_id) REFERENCES user_feedback_forms(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES feedback_questions(id) ON DELETE CASCADE,
    INDEX idx_feedback_form (user_feedback_form_id),
    INDEX idx_question_id (question_id)
);
