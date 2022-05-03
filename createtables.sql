DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Cocktail;
DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS Taste;
DROP TABLE IF EXISTS Ingredient_Cocktail;
DROP TABLE IF EXISTS Saved_Cocktail;

CREATE TABLE IF NOT EXISTS `User` (
  `user_id` int(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `User` (`user_id`, `name`,`username`,`password`) VALUES
(1,"Jane Street","janestreet1","password1"),
(2,"John Doe","johndoe1","password2"),
(3,"Dev Chauhan","devchauhan3","password3");

CREATE TABLE IF NOT EXISTS `Cocktail` (
  `cocktail_id` int(10) NOT NULL,
  `cocktail_name` varchar(50) NOT NULL,
  `user_id` int(10) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `taste_id` int(10) NOT NULL,
  `likes` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Cocktail` (`cocktail_id`, `cocktail_name`,`user_id`, `description`, `taste_id`,`likes`) VALUES
(1, "Whiskey Sour", 1,"The whiskey sour is a mixed drink containing whiskey (often bourbon), lemon juice, and sugar", 1, 0),
(2, "Boston Sour", 2,"The Boston sour is a mixed drink containing whiskey (often bourbon), lemon juice, sugar, and a dash of egg white .", 1, 0);

CREATE TABLE IF NOT EXISTS `Ingredient` (
  `ingredient_id` int(10) NOT NULL,
  `ingredient_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Ingredient` (`ingredient_id`, `ingredient_name`) VALUES
(1,"Bourbon"),
(2,"Lemon juice"),
(3,"Simple syrup"),
(4,"Orange"),
(5,"Maraschino cherry"),
(6,"Egg whites");

CREATE TABLE IF NOT EXISTS `Taste` (
  `taste_id` int(10) NOT NULL,
  `taste_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Taste` (`taste_id`,`taste_name`) VALUES
(1,"Sour"),
(2,"Bitter");

CREATE TABLE IF NOT EXISTS `Ingredient_Cocktail` (
  `ingredient_id` int(10) NOT NULL,
  `cocktail_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Ingredient_Cocktail` (`ingredient_id`,`cocktail_id`) VALUES
(1,1),
(2,1),
(3,1),
(4,1),
(5,1),
(1,2),
(2,2),
(3,2),
(4,2),
(5,2),
(6,2);

CREATE TABLE IF NOT EXISTS `Saved_Cocktail` (
  `cocktail_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Saved_Cocktail` (`cocktail_id`,`user_id`) VALUES
(1,1),
(1,2);


DELIMITER //
CREATE PROCEDURE ReturnAllCocktails()
BEGIN
    SELECT c.cocktail_id, c.cocktail_name, u.name, c.description, t.taste_name, c.likes FROM Cocktail c, User u, Taste t WHERE u.user_id = c.user_id AND t.taste_id = c.taste_id;
END //
    
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SortByLikes()
BEGIN
    SELECT c.cocktail_id, c.cocktail_name, u.name, c.description, t.taste_name, c.likes FROM Cocktail c, User u, Taste t WHERE u.user_id = c.user_id AND t.taste_id = c.taste_id ORDER BY c.likes;
END //
    
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SortByTaste()
BEGIN
    SELECT c.cocktail_id, c.cocktail_name, u.name, c.description, t.taste_name, c.likes FROM Cocktail c, User u, Taste t WHERE u.user_id = c.user_id AND t.taste_id = c.taste_id ORDER BY c.taste_id;
END //
    
DELIMITER ;