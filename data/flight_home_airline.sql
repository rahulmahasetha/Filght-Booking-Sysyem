-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: flight
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `home_airline`
--

LOCK TABLES `home_airline` WRITE;
/*!40000 ALTER TABLE `home_airline` DISABLE KEYS */;
INSERT INTO `home_airline` VALUES (1,'American Airlines','AA','airlines/American-Airlines-Logo.png'),
  (2,'British Airways','BA','airlines/British-Airways-Logo-1997-present.jpg'),
  (3,'Emirates','EK','airlines/Emirates-Logo-1985.jpg'),
  (4,'Singapore Airlines','SQ','airlines/R.jfif'),
  (5,'Japan Airlines','JL','airlines/japan-airlines-logo.png'),
  (6,'Lufthansa','LH','airlines/Lufthansa-Logo-1953-1963.png'),
  (7,'Air France','AF','airlines/OIP.jfif'),
  (8,'Qatar Airways','QR','airlines/Qatar-Airways-Logo-2006-present.jpg'),
  (9,'Cathay Pacific','CX','airlines/Cathay-Pacific-Logo.png'),
  (10,'Qantas','QF','airlines/Qantas-Logo.png'),
  (11,'Nepal Airlines','NA','airlines/R.png'),
  (12,'Indigo','IG','airlines/IndiGo-Logo.wine.png'),
  (13,'Air India','AI','airlines/OIP_2.jfif');
/*!40000 ALTER TABLE `home_airline` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-14 12:19:01
