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
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-02 09:07:11.213073'),(2,'auth','0001_initial','2025-04-02 09:07:12.232654'),(3,'admin','0001_initial','2025-04-02 09:07:12.461146'),(4,'admin','0002_logentry_remove_auto_add','2025-04-02 09:07:12.476180'),(5,'admin','0003_logentry_add_action_flag_choices','2025-04-02 09:07:12.489909'),(6,'contenttypes','0002_remove_content_type_name','2025-04-02 09:07:12.627337'),(7,'auth','0002_alter_permission_name_max_length','2025-04-02 09:07:12.731356'),(8,'auth','0003_alter_user_email_max_length','2025-04-02 09:07:12.772543'),(9,'auth','0004_alter_user_username_opts','2025-04-02 09:07:12.787022'),(10,'auth','0005_alter_user_last_login_null','2025-04-02 09:07:12.878814'),(11,'auth','0006_require_contenttypes_0002','2025-04-02 09:07:12.884230'),(12,'auth','0007_alter_validators_add_error_messages','2025-04-02 09:07:12.894514'),(13,'auth','0008_alter_user_username_max_length','2025-04-02 09:07:13.016344'),(14,'auth','0009_alter_user_last_name_max_length','2025-04-02 09:07:13.146005'),(15,'auth','0010_alter_group_name_max_length','2025-04-02 09:07:13.183427'),(16,'auth','0011_update_proxy_permissions','2025-04-02 09:07:13.197614'),(17,'auth','0012_alter_user_first_name_max_length','2025-04-02 09:07:13.315217'),(23,'sessions','0001_initial','2025-04-02 09:07:15.477433'),(27,'home','0001_initial','2025-04-05 18:45:34.313265'),(28,'home','0002_contact_date_alter_contact_message','2025-04-05 18:45:34.319123'),(29,'home','0003_rename_name_contact_name1','2025-04-05 18:45:34.322637'),(30,'home','0004_rename_name1_contact_name','2025-04-05 18:45:34.325769'),(31,'home','0005_airline_airport_flight_booking_passenger_payment','2025-04-05 18:45:34.330079'),(32,'home','0006_remove_booking_user_user','2025-04-05 18:45:34.333603'),(33,'home','0007_booking_user_delete_user','2025-04-05 18:45:34.337126'),(34,'home','0008_alter_booking_user','2025-04-05 18:45:34.341509'),(35,'home','0009_remove_booking_passengers_and_more','2025-04-05 18:45:34.347606'),(36,'home','0010_populate_booking_users','2025-04-05 18:45:34.351933'),(37,'home','0011_alter_airline_logo_alter_airport_image_and_more','2025-04-05 18:45:34.356012'),(38,'home','0012_remove_payment_amount_remove_payment_payment_date_and_more','2025-04-05 18:45:34.359310'),(39,'home','0013_payment_amount_payment_payment_date_payment_status_and_more','2025-04-05 18:45:34.363684'),(40,'home','0014_alter_payment_amount_alter_payment_status','2025-04-05 18:45:34.366835'),(41,'home','0015_remove_booking_contact_email_and_more','2025-04-05 18:45:34.370176'),(42,'home','0016_booking_num_passengers','2025-04-05 18:45:34.374377'),(43,'home','0017_remove_booking_num_passengers','2025-04-05 18:45:34.379273'),(44,'home','0018_alter_passenger_booking','2025-04-05 18:45:34.382867'),(45,'home','0019_booking_nums_passengers_alter_passenger_booking','2025-04-05 18:45:34.386671'),(46,'home','0020_alter_booking_nums_passengers_and_more','2025-04-08 13:42:29.004584');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
