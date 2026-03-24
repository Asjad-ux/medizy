-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: railway
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
-- Table structure for table `medical_stores`
--

DROP TABLE IF EXISTS `medical_stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_stores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `image_url` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_stores`
--

LOCK TABLES `medical_stores` WRITE;
/*!40000 ALTER TABLE `medical_stores` DISABLE KEYS */;
INSERT INTO `medical_stores` VALUES (1,'Max Help Pharmacy',28.500542440262265,77.29049632882733,'assets/pharmacies/1.jpg'),(2,'Apollo Pharmacy Alaknanda',28.524873706165184,77.25424234568577,'assets/pharmacies/2.jpg'),(3,'Brahmastra Pharmacy',28.536321944341864,77.26621708015468,'assets/pharmacies/3.jpg'),(4,'Bharat Pharmacy',28.510729835762945,77.23703801215854,'assets/pharmacies/4.jpg'),(5,'HealthCare Pharmacy',28.511005364069913,77.23704070664479,'assets/pharmacies/5.jpg'),(6,'A 1 Pharmacy',28.498672788781633,77.29541127696736,'assets/pharmacies/6.jpg'),(7,'The Helpline Pharmacy',28.528780018799996,77.21115884133363,'assets/pharmacies/7.jpg'),(8,'All India Medical Store',28.499787438553817,77.29182237483636,'assets/pharmacies/8.jpg'),(9,'Irex Pharmacy',28.5287555422563,77.21028252948528,'assets/pharmacies/9.jpg'),(10,'Sanjivani',28.5149404826063,77.23389507363248,'assets/pharmacies/10.jpg');
/*!40000 ALTER TABLE `medical_stores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicines`
--

DROP TABLE IF EXISTS `medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store_id` int DEFAULT NULL,
  `medicine_name` varchar(100) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicines`
--

LOCK TABLES `medicines` WRITE;
/*!40000 ALTER TABLE `medicines` DISABLE KEYS */;
INSERT INTO `medicines` VALUES (1,1,'Paracetamol',20,45),(2,1,'Crocin',30,12),(3,1,'Dolo 650',25,60),(4,1,'Azithromycin',80,15),(5,1,'Vitamin C',50,40),(6,1,'ORS',20,100),(7,1,'Ibuprofen',35,25),(8,1,'Cough Syrup',90,18),(9,1,'Zinc Tablets',70,22),(10,1,'Amoxicillin',120,10),(11,2,'Paracetamol',22,30),(12,2,'Crocin',28,20),(13,2,'ORS',18,80),(14,2,'Dolo 650',27,55),(15,2,'Vitamin D',60,35),(16,2,'Cough Syrup',95,10),(17,2,'Ibuprofen',40,28),(18,2,'Metformin',110,15),(19,2,'Aspirin',20,50),(20,2,'Ranitidine',45,18),(21,3,'Paracetamol',21,33),(22,3,'Crocin',29,19),(23,3,'ORS',22,120),(24,3,'Dolo 650',26,40),(25,3,'Vitamin C',55,50),(26,3,'Cough Syrup',100,25),(27,3,'Zinc Tablets',65,30),(28,3,'Insulin',250,8),(29,3,'Thyroxine',90,12),(30,3,'Amoxicillin',130,6),(31,4,'Paracetamol',21,33),(32,4,'Crocin',29,19),(33,4,'ORS',19,95),(34,4,'Azithromycin',88,11),(35,4,'Vitamin D',58,26),(36,4,'Ibuprofen',36,23),(37,4,'Cough Syrup',92,14),(38,4,'Diclofenac',40,20),(39,4,'Loratadine',35,22),(40,4,'Pantoprazole',95,9),(41,4,'Paracetamol',23,41),(42,4,'Crocin',31,22),(43,4,'Dolo 650',21,110),(44,4,'Vitamin C',53,37),(45,4,'Ibuprofen',39,27),(46,5,'Ibuprofen',39,27),(47,5,'Zinc Tablets',74,19),(48,5,'Amoxicillin',125,9),(49,5,'Metformin',115,11),(50,5,'Aspirin',22,44),(51,6,'Paracetamol',19,60),(52,6,'Crocin',27,18),(53,6,'ORS',17,105),(54,6,'Azithromycin',82,17),(55,6,'Vitamin D',59,21),(56,6,'Ibuprofen',34,26),(57,6,'Cough Syrup',89,20),(58,6,'Ranitidine',48,15),(59,6,'Cetrizine',28,35),(60,6,'Diclofenac',42,18),(61,7,'Paracetamol',24,38),(62,7,'Crocin',33,15),(63,7,'ORS',23,98),(64,7,'Dolo 650',29,44),(65,7,'Vitamin C',57,42),(66,7,'Ibuprofen',41,29),(67,7,'Zinc Tablets',76,17),(68,7,'Thyroxine',260,6),(69,7,'Loratidine',38,21),(70,8,'Paracetamol',20,55),(71,8,'Crocin',30,21),(72,8,'ORS',19,115),(73,8,'Azithromycin',86,16),(74,8,'Vitamin D',62,28),(75,8,'Cough Syrup',37,32),(76,8,'Pantoprazole',94,11),(77,8,'Metformin',120,13),(78,8,'Aspirin',25,36),(79,9,'Paracetamol',22,48),(80,9,'Crocin',34,17),(81,9,'ORS',20,102),(82,9,'Dolo 650',27,36),(83,9,'Vitamin C',54,33),(84,9,'Ibuprofen',40,25),(85,9,'Zinc Tablets',73,16),(86,9,'Amoxicillin',128,6),(87,9,'Ranitidine',50,12),(88,9,'Cetirizine',30,28),(89,10,'Paracetamol',21,52),(90,10,'Crocin',29,23),(91,10,'ORS',18,108),(92,10,'Azithromycin',89,14),(93,10,'Vitamin D',61,29),(94,10,'Ibuprofen',35,31),(95,10,'Cough Syrup',96,12),(96,10,'Pantoprazole',98,16),(97,10,'Diclofenac',45,19),(98,10,'Loratadine',37,24);
/*!40000 ALTER TABLE `medicines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `online_prices_wide`
--

DROP TABLE IF EXISTS `online_prices_wide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `online_prices_wide` (
  `id` int NOT NULL AUTO_INCREMENT,
  `medicine_name` varchar(100) DEFAULT NULL,
  `PharmEasy` int DEFAULT NULL,
  `NetMeds` int DEFAULT NULL,
  `TATA1mg` int DEFAULT NULL,
  `DawaIndia` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `online_prices_wide`
--

LOCK TABLES `online_prices_wide` WRITE;
/*!40000 ALTER TABLE `online_prices_wide` DISABLE KEYS */;
INSERT INTO `online_prices_wide` VALUES (1,'Paracetamol',23,7,9,23),(2,'Crocin',15,18,19,14),(3,'Dolo 650',23,26,29,30),(4,'Dolo 650',92,42,114,40),(5,'Vitamin C',20,22,22,22),(6,'ORS',21,21,9,32),(7,'Ibuprofen',19,23,25,9),(8,'Cough Syrup',116,140,109,75),(9,'Zinc Tablets',60,58,59,55),(10,'Amoxicillin',110,105,108,100),(11,'Vitamin D',70,68,69,65),(12,'Metformin',45,42,44,40),(13,'Aspirin',30,28,29,26),(14,'Ranitidine',55,52,54,50),(15,'Insulin',350,340,345,330),(16,'Thyroxine',65,62,64,60),(17,'Diclofenac',48,45,47,42),(18,'Loratadine',52,50,51,48),(19,'Pantoprazole',75,72,74,70),(20,'Cetirizine',28,26,27,24);
/*!40000 ALTER TABLE `online_prices_wide` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharmacies`
--

DROP TABLE IF EXISTS `pharmacies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharmacies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `gst` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharmacies`
--

LOCK TABLES `pharmacies` WRITE;
/*!40000 ALTER TABLE `pharmacies` DISABLE KEYS */;
INSERT INTO `pharmacies` VALUES (1,'asjad','sc','6544');
/*!40000 ALTER TABLE `pharmacies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile`
--

LOCK TABLES `user_profile` WRITE;
/*!40000 ALTER TABLE `user_profile` DISABLE KEYS */;
INSERT INTO `user_profile` VALUES (1,'asjad7zia@gmail.com','8826293248','asjad88262'),(2,'jollyllbkalamba@gmail.com','8826293248','zia1234'),(3,'zohra.zia@gmail.com','9810906056','zohra88262'),(4,'togizenen2@gmail.com','9560223728','Toji zenin');
/*!40000 ALTER TABLE `user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-24 22:51:49
