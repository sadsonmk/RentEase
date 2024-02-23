CREATE DATABASE IF NOT EXISTS 'rent-ease';

CREATE TABLE `rent-ease`.`users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `full_name` VARCHAR(200) NOT NULL,
    `email` VARCHAR(150) NOT NULL,
    `phone_number` VARCHAR(15) NOT NULL,
    `password` VARCHAR(500) NOT NULL,
    `verification_status` INT(0) NOT NULL,
    `profile_picture` BLOB NOT NULL,
    `bio` VARCHAR(1000) NOT NULL,
    `user_role` INT(0) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `rent-ease`.`property` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL ,
    `tiltle` VARCHAR(50) NOT NULL,
    `description` VARCHAR(1000) NOT NULL,
    `location` VARCHAR(500) DEFAULT NULL,
    `address` VARCHAR(500) NOT NULL,
    `type` VARCHAR(45) NOT NULL,
    `picture` BLOB NOT NULL,
    `price` DOUBLE NOT NULL,
    `rating` INT NOT NULL ,
    `availability` INT NOT NULL ,
    `miscellaneous` VARCHAR(1000) DEFAULT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE `rent-ease`.`review` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL ,
    `property_id` INT NOT NULL ,
    `comment` VARCHAR(1000) NOT NULL,
    `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `rating` INT NOT NULL ,
    `availability` INT NOT NULL ,
    `miscellaneous` VARCHAR(1000) DEFAULT NULL,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`property_id`) REFERENCES `property`(`id`),
    PRIMARY KEY (`id`)
);