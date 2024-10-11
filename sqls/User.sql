CREATE TABLE user
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(100) not null,
    email varchar(40) not null,
    password text
);