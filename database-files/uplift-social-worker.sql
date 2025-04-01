-- As a social worker, I need to be able to create a profile for my organization so that it can be
-- viewed by individuals.
INSERT INTO organizations VALUES
('EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE', 'Healthcare Access',
 'Expanding healthcare access to underserved populations', 'https://hap.org',
 FALSE, NULL, '2024-01-05 13:00:00', '2024-01-05 13:00:00');

-- As a social worker, I need to be able to update and edit our organization profile so that users
-- can be up to date with the most recent developments in our organization.
UPDATE organizations
SET description = 'Healthcare Access is a nonprofit organization dedicated to expanding equitable
healthcare for underserved communities. By providing comprehensive medical services, promoting health
education, and advocating for policy change, we work to eliminate barriers to quality care.',
    website_url = 'https://healthcareaccess.org'
WHERE id = 'EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE';

INSERT INTO programs VALUES
('DDDDDD44-4444-4444-4444-DDDDDD444444', 'Health Checkup Camps',
 'Provide free or low-cost blood pressure, glucose, and cholesterol screenings.',
 'close', '2023-07-01', '2023-12-31 23:59:59', '2024-01-31',
 'EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE', 'IIIIIIII-IIII-IIII-IIII-IIIIIIIIIIII',
 '2024-07-20 13:00:00', '2024-07-21 09:00:00');


-- As a social worker, I need to be able to receive results from user feedback forms so that my
-- organization can work to improve our future operations based on that feedback.
INSERT INTO feedback_forms VALUES
('GGGGGG77-7777-7777-7777-GGGGGG777777', 'DDDDDD44-4444-4444-4444-DDDDDD444444',
 '55555555-5555-5555-5555-555555555555', 'Program Feedback Form', '2024-07-25 10:25:00',
 '2024-07-25 10:25:00', 4, 4, 5, 5,
 'It was a really great program, no notes.' );

SELECT * FROM feedback_forms WHERE program_id = 'DDDDDD44-4444-4444-4444-DDDDDD444444';

-- As a social worker, I need to be able to add new programs that our organization is offering so the
-- new programs can be made visible to users who may benefit from them.

INSERT INTO programs VALUES
('OOOOOOOO-OOOO-OOOO-OOOO-OOOOOOOOOOOO', 'Healthcare Subsidy',
 'Subsidies for medical care for low-income individuals', 'open',
 '2024-01-20', '2024-12-31 23:59:59', '2025-12-31',
 'EEEEEEEE-EEEE-EEEE-EEEE-EEEEEEEEEEEE', 'IIIIIIII-IIII-IIII-IIII-IIIIIIIIIIII',
 '2024-01-13 12:00:00', '2024-01-13 12:00:00');


-- As a social worker, I need to be able to find direct contacts of other organizations on the platform
-- so that we can talk about potential collaboration opportunities.

SELECT * FROM point_of_contacts
WHERE contact_type = 'organization';

-- As a social worker, I need to be able to add the organization’s point of contact so my organization
-- can be contacted if users have any questions regarding the programs my organization offers.

INSERT INTO point_of_contacts VALUES
('AZBDZARC-SVZZ-ZZDZ-Z159-XXHZLPKZPZZO', 'organization',
 'ee8c8555-45d6-4a2a-8a00-1d4c851358f3', 'Program Coordinator',
 'caseycat@healthcareaccess.org', '894-309-2748', '2025-01-14 18:03:42',
 '2025-01-14 18:10:12');

