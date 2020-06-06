CREATE DATABASE IF NOT EXISTS food_storage;
USE food_storage;

CREATE TABLE `fridge_storage` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `EAN` bigint,
  `amount` int,
  `expiredate` date
);

CREATE TABLE `item_name` (
  `ingredient` varchar(255) PRIMARY KEY
);

CREATE TABLE `freezer_storage` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `EAN` bigint,
  `amount` int,
  `expiredate` date
);

CREATE TABLE `item` (
  `EAN` bigint PRIMARY KEY,
  `ingredient` varchar(255),
  `default_amount` int
);

CREATE TABLE `dry_storage` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `EAN` bigint,
  `amount` int,
  `expiredate` date
);


ALTER TABLE `item` ADD FOREIGN KEY (`ingredient`) REFERENCES `item_name` (`ingredient`);

ALTER TABLE `fridge_storage` ADD FOREIGN KEY (`EAN`) REFERENCES `item` (`EAN`);

ALTER TABLE `freezer_storage` ADD FOREIGN KEY (`EAN`) REFERENCES `item` (`EAN`);

ALTER TABLE `dry_storage` ADD FOREIGN KEY (`EAN`) REFERENCES `item` (`EAN`);
