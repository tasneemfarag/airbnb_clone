''' Creates the database users '''
CREATE USER 'airbnb_user_test'
    IDENTIFIED BY '@@@@dummy';

''' Created the dev and prod databases '''
CREATE DATABASE airbnb_test
    DEFAULT CHARACTER SET = utf8
    DEFAULT COLLATE = utf8_general_ci;

''' Grants privileges to users on their respective databases '''
GRANT ALL PRIVILEGES ON airbnb_test.*
    TO 'airbnb_user_test';
