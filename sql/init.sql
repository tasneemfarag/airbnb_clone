CREATE USER 'airbnb_user_dev'
    IDENTIFIED BY 'dummy@@@';
CREATE USER 'airbnb_user_prod'@'localhost'
    IDENTIFIED BY 'try_again!!!';
CREATE DATABASE airbnb_dev
    DEFAULT CHARACTER SET = utf8
    DEFAULT COLLATE = utf8_general_ci;
CREATE DATABASE airbnb_prod
    DEFAULT CHARACTER SET = utf8
    DEFAULT COLLATE = utf8_general_ci;
GRANT ALL PRIVILEGES ON airbnb_dev.*
    TO 'airbnb_user_dev';
GRANT ALL PRIVILEGES ON airbnb_prod.*
    TO 'airbnb_user_prod'@'localhost';
