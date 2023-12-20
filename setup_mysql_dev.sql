-- Script that prepares development setup on a MySQL server for the AirBnB clone project

-- Create the development database
CREATE DATABASE
IF NOT EXISTS
`hbnb_dev_db`;

-- Create the development user
CREATE USER
IF NOT EXISTS
'hbnb_dev'@'localhost'
IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant user 'hbnb_dev'@'localhost' ALL privileges on the database "hbnb_dev_db"
GRANT ALL
ON `hbnb_dev_db`.*
TO 'hbnb_dev'@'localhost';

-- Grant user 'hbnb_dev'@'localhost' SELECT privileges on the database "performance_schema"
GRANT SELECT
ON `performance_schema`.*
TO 'hbnb_dev'@'localhost';
