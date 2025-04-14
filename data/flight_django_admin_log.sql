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
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-04-08 17:43:46.403918','1','American Airlines',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(2,'2025-04-08 17:46:22.039643','2','British Airways',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(3,'2025-04-08 17:49:15.344797','3','Emirates',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(4,'2025-04-08 17:50:05.976768','4','Singapore Airlines',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(5,'2025-04-08 17:50:51.760176','5','Japan Airlines',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(6,'2025-04-08 17:51:25.535918','6','Lufthansa',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(7,'2025-04-08 17:51:59.918128','7','Air France',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(8,'2025-04-08 17:52:28.194405','8','Qatar Airways',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(9,'2025-04-08 17:53:06.309097','9','Cathay Pacific',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(10,'2025-04-08 17:53:35.416375','10','Qantas',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(11,'2025-04-08 17:54:09.234775','11','Nepal Airlines',2,'[{\"changed\": {\"fields\": [\"Logo\"]}}]',2,3),(12,'2025-04-08 17:55:26.019774','5','Tokyo (HND)',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',3,3),(13,'2025-04-08 17:59:14.776157','12','Indigo',1,'[{\"added\": {}}]',2,3),(14,'2025-04-08 18:00:41.033849','13','Air India',1,'[{\"added\": {}}]',2,3),(15,'2025-04-08 18:02:55.265953','6','New Delhi (DEL)',1,'[{\"added\": {}}]',3,3),(16,'2025-04-08 18:03:29.617121','7','Mumbai (BOM)',1,'[{\"added\": {}}]',3,3),(17,'2025-04-08 18:04:14.544763','8','Hyderabad (HYD)',1,'[{\"added\": {}}]',3,3),(18,'2025-04-08 18:04:47.486577','9','Kolkata (CCU)',1,'[{\"added\": {}}]',3,3),(19,'2025-04-08 18:05:16.778736','10','Chennai (MAA)',1,'[{\"added\": {}}]',3,3),(20,'2025-04-08 18:07:17.028594','11','Varanasi (VNS)',1,'[{\"added\": {}}]',3,3),(21,'2025-04-08 18:08:56.686651','12','pune (PUN)',1,'[{\"added\": {}}]',3,3),(22,'2025-04-08 18:09:34.063781','13','Darbhanga (DBR)',1,'[{\"added\": {}}]',3,3),(23,'2025-04-08 18:10:10.258062','14','Patna (PAT)',1,'[{\"added\": {}}]',3,3),(24,'2025-04-08 18:13:03.076808','15','Vijayawada (VGA)',1,'[{\"added\": {}}]',3,3),(25,'2025-04-08 18:16:57.118399','21','AIAI 126',1,'[{\"added\": {}}]',4,3),(26,'2025-04-08 18:20:23.914907','22','IGAI 128',1,'[{\"added\": {}}]',4,3),(27,'2025-04-08 18:24:21.326107','16','Kathmandu (KTM)',1,'[{\"added\": {}}]',3,3),(28,'2025-04-08 18:26:50.367406','17','Bhairahawa (BHR)',1,'[{\"added\": {}}]',3,3),(29,'2025-04-08 18:29:09.073691','23','NANP 703',1,'[{\"added\": {}}]',4,3),(30,'2025-04-08 18:30:50.805413','24','NANA1154',1,'[{\"added\": {}}]',4,3),(31,'2025-04-08 18:33:41.874561','25','AI403',1,'[{\"added\": {}}]',4,3),(32,'2025-04-08 18:33:49.497844','24','NA1154',2,'[{\"changed\": {\"fields\": [\"Flight number\"]}}]',4,3),(33,'2025-04-08 18:33:56.902169','23','NA703',2,'[{\"changed\": {\"fields\": [\"Flight number\"]}}]',4,3);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
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
