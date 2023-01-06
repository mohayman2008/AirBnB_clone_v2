-- Script that prepares test setup on a MySQL server for the AirBnB clone project

-- Create the test database
CREATE DATABASE
IF NOT EXISTS
`hbnb_test_db`;

-- Create the test user
CREATE USER
IF NOT EXISTS
'hbnb_test'@'localhost'
IDENTIFIED BY 'hbnb_test_pwd';

-- Grant user 'hbnb_test'@'localhost' ALL privileges on the database "hbnb_test_db"
GRANT ALL
ON `hbnb_test_db`.*
TO 'hbnb_test'@'localhost';

-- Grant user 'hbnb_test'@'localhost' SELECT privileges on the database "performance_schema"
GRANT SELECT
ON `performance_schema`.*
TO 'hbnb_test'@'localhost';
