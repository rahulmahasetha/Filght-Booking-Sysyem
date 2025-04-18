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
-- Dumping data for table `home_airport`
--

LOCK TABLES `home_airport` WRITE;
/*!40000 ALTER TABLE `home_airport` DISABLE KEYS */;
INSERT INTO `home_airport` VALUES (1,'JFK','John F. Kennedy International Airport','New York','USA',NULL),
  (2,'LHR','Heathrow Airport','London','UK',NULL),
  (3,'DXB','Dubai International Airport','Dubai','UAE',NULL),
  (4,'SIN','Singapore Changi Airport','Singapore','Singapore',NULL),
  (5,'HND','Haneda Airport','Tokyo','Japan','airports/OIP_1.jfif'),
  (6,'DEL','Indira Gandhi International Airport','New Delhi','India',''),
  (7,'BOM','Chhatrapati Shivaji Maharaj International Airport','Mumbai','India',''),
  (8,'HYD','Rajiv Gandhi International Airport','Hyderabad','India',''),
  (9,'CCU','Netaji Subhas Chandra Bose International Airport','Kolkata','India',''),
  (10,'MAA','Chennai International Airport','Chennai','India',''),
  (11,'VNS','Lal Bahadur Shastri International Airport','Varanasi','India',''),
  (12,'PUN','Pune Airport','pune','India',''),
  (13,'DBR','Darbhanga Airport','Darbhanga','India',''),
  (14,'PAT','Jay Prakash Narayan International Airport','Patna','India',''),
  (15,'VGA','​Vijayawada International Airport,','Vijayawada','India',''),
  (16,'KTM','Tribhuvan International Airport','Kathmandu','Nepal',''),
  (17,'BHR','Gautam Buddha Airport','Bhairahawa','Nepal','');
/*!40000 ALTER TABLE `home_airport` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-14 12:19:00
