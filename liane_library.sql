-- MySQL dump 10.13  Distrib 8.0.45, for macos15 (arm64)
--
-- Host: localhost    Database: liane_library
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `comments` text,
  `is_available` tinyint(1) NOT NULL DEFAULT '1',
  `date_added` date DEFAULT (curdate()),
  PRIMARY KEY (`book_id`),
  UNIQUE KEY `isbn` (`isbn`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'Atomic Habits','James Clear','9780735211292','Self-Help','Popular productivity book',1,'2025-01-10'),(2,'The Alchemist','Paulo Coelho','9780061122415','Fantasy','Inspirational novel',1,'2025-01-15'),(3,'1984','George Orwell','9780451524935','Dystopian','Classic dystopian fiction',0,'2025-02-01'),(4,'Pride and Prejudice','Jane Austen','9780141439518','Romance','Classic romance novel',1,'2025-02-10'),(5,'The Hobbit','J.R.R. Tolkien','9780547928227','Fantasy','Adventure fantasy',0,'2025-02-20'),(6,'Sapiens','Yuval Noah Harari','9780062316097','History','History of humankind',0,'2025-03-01'),(7,'Dune','Frank Herbert','9780441172719','Science Fiction','Epic sci-fi novel',0,'2025-03-12'),(8,'The Psychology of Money','Morgan Housel','9780857197689','Finance','Money management insights',1,'2025-03-20'),(9,'To Kill a Mockingbird','Harper Lee','9780061120084','Fiction','Pulitzer Prize winner',1,'2025-04-01'),(10,'The Catcher in the Rye','J.D. Salinger','9780316769488','Classic','Coming-of-age story',1,'2025-04-10'),(11,'Harry Potter and the Philosopher\'s Stone','J.K. Rowling','9780747532743','Fantasy','First book in the series',0,'2026-05-29'),(13,'A Brief History of Time','Stephen Hawking','9780553380163','Science','',0,'2026-06-01'),(14,'Deep Work','Cal Newport','9781455586691','Productivity','',1,'2026-06-01'),(16,'Wings of Fire','A.P.J. Abdul Kalam','9788173711466','Autobiography','',1,'2026-06-01'),(17,'The Silent Patient','Alex Michaelides','9781250301697','Thriller','',1,'2026-06-01'),(18,'The Kite Runner','Khaled Hosseini','9781594631931','Fiction, Fantasy','',1,'2026-06-01'),(20,'Rebecca','Daphne du Maurier','9780380730407','Gothic Fiction','',1,'2026-06-01'),(22,'The Midnight Library','Matt Haig','9780525559474','Fiction','',1,'2026-06-05'),(23,'Thinking, Fast and Slow','Daniel Kahneman','9780374533557','Psychology','',1,'2026-06-05'),(24,'Gone Girl','Gillian Flynn','9780307588371','Mystery','',1,'2026-06-05');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friends`
--

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friends` (
  `friend_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `max_loan` tinyint DEFAULT '2',
  `notes` text,
  PRIMARY KEY (`friend_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friends`
--

LOCK TABLES `friends` WRITE;
/*!40000 ALTER TABLE `friends` DISABLE KEYS */;
INSERT INTO `friends` VALUES (1,'Emma','Wilson','emma@email.com','5551001',2,'Returns books on time'),(2,'Liam','Brown','liam@email.com','5551002',3,'Fantasy fan'),(3,'Olivia','Davis','olivia@email.com','5551003',2,NULL),(4,'Noah','Miller','noah@email.com','5551004',2,'Likes history books'),(5,'Sophia','Moore','sophia@email.com','5551005',4,NULL),(6,'James','Taylor','james@email.com','5551006',2,'Frequent borrower'),(7,'Ava','Anderson','ava@email.com','5551007',3,NULL),(8,'Lucas','Thomas','lucas@email.com','5551008',2,'Enjoys classics'),(9,'Mia','Jackson','mia@email.com','5551009',2,'Adventure lover'),(10,'Ethan','White','ethan@email.com','5551010',5,'Book club member'),(13,'Ann','Marie','annmarie@hotmail.com','+49 15132186',2,NULL);
/*!40000 ALTER TABLE `friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `loan_id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `friend_id` int NOT NULL,
  `date_borrowed` date DEFAULT (curdate()),
  `due_date` date DEFAULT NULL,
  `date_returned` date DEFAULT NULL,
  `loan_status` varchar(20) DEFAULT 'BORROWED',
  `remarks` text,
  PRIMARY KEY (`loan_id`),
  KEY `fk_loans_books` (`book_id`),
  KEY `fk_loans_friends` (`friend_id`),
  CONSTRAINT `fk_loans_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`),
  CONSTRAINT `fk_loans_friends` FOREIGN KEY (`friend_id`) REFERENCES `friends` (`friend_id`),
  CONSTRAINT `chk_due_date` CHECK ((`due_date` >= `date_borrowed`)),
  CONSTRAINT `chk_status` CHECK ((`loan_status` in (_utf8mb4'BORROWED',_utf8mb4'RETURNED',_utf8mb4'OVERDUE')))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (1,2,1,'2025-05-01','2025-05-15','2025-05-12','RETURNED','Returned early'),(2,5,2,'2025-05-03','2025-05-17','2026-06-01','RETURNED','Returned in good condition'),(3,7,3,'2025-05-05','2025-05-19',NULL,'OVERDUE','Reminder sent'),(4,1,4,'2025-05-08','2025-05-22','2025-05-20','RETURNED',NULL),(5,3,5,'2025-05-10','2025-05-24',NULL,'BORROWED',NULL),(6,4,6,'2025-05-11','2025-05-25','2025-05-24','RETURNED',NULL),(7,6,7,'2025-05-12','2025-05-26',NULL,'BORROWED','First loan'),(8,8,8,'2025-05-13','2025-05-27','2025-05-26','RETURNED',NULL),(10,11,9,'2026-05-29','2026-07-15',NULL,'BORROWED','Testing loan function'),(13,13,13,'2026-06-01','2026-06-15',NULL,'BORROWED',''),(15,20,13,'2026-06-01','2026-06-15',NULL,'BORROWED',''),(19,8,13,'2026-06-01','2026-06-15','2026-06-01','RETURNED','');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-09  8:49:22
