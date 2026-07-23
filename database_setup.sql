-- Run this once in MySQL before starting the Django backend.
-- Django's `migrate` command will create all the tables automatically;
-- this script just creates the database and a dedicated user.

CREATE DATABASE IF NOT EXISTS college_chatbot_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Optional: create a dedicated MySQL user instead of using root
-- CREATE USER 'college_bot_user'@'localhost' IDENTIFIED BY 'strong_password_here';
-- GRANT ALL PRIVILEGES ON college_chatbot_db.* TO 'college_bot_user'@'localhost';
-- FLUSH PRIVILEGES;

USE college_chatbot_db;
