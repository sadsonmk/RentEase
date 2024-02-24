-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS `rent_ease_db`;
CREATE USER IF NOT EXISTS `dev`@`localhost` IDENTIFIED BY 'dev_pwd';
GRANT ALL PRIVILEGES ON `rent_ease_db`.* TO `dev`@`localhost`;
GRANT SELECT ON `performance_schema`.* TO `dev`@`localhost`;
FLUSH PRIVILEGES;