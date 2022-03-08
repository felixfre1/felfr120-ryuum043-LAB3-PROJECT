--
-- File generated with SQLiteStudio v3.3.3 on fre feb. 18 16:33:22 2022
--
-- Text encoding used: UTF-8
--
-- PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: sign_up
CREATE TABLE sign_up (email STRING NOT NULL UNIQUE, user_password STRING NOT NULL, firstname STRING  NOT NULL, familyname STRING NOT NULL, gender STRING NOT NULL, city STRING NOT NULL, country STRING NOT NULL, token STRING NOT NULL,primary key(email));

-- Table: user_communication
CREATE TABLE user_communication (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, sender_email STRING NOT NULL, receiver_email STRING NOT NULL, post_message STRING NOT NULL, post_timestamp STRING NOT NULL, country STRING NOT NULL, city STRING NOT NULL);

COMMIT TRANSACTION;
-- PRAGMA foreign_keys = on;
