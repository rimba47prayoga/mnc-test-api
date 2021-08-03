-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: mnc_test
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.20.04.2

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
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `user_id` varchar(100) DEFAULT NULL,
  `payment_id` varchar(100) NOT NULL,
  `amount` int DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  `balance_before` int DEFAULT NULL,
  `balance_after` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES ('5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','30902446-a242-4217-b6c6-35dcd615fd4d',100000,'Pulsa Telkomsel 100k',870000,770000,'2021-08-03 21:04:55'),('5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','ea8405dd-93c4-4ebc-9f1c-85250ebf1e72',100000,'Pulsa Telkomsel 100k',1000000,900000,'2021-08-03 20:56:38');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topup`
--

DROP TABLE IF EXISTS `topup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topup` (
  `user_id` varchar(100) DEFAULT NULL,
  `top_up_id` varchar(100) NOT NULL,
  `amount_top_up` int DEFAULT NULL,
  `balance_before` int DEFAULT NULL,
  `balance_after` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`top_up_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topup`
--

LOCK TABLES `topup` WRITE;
/*!40000 ALTER TABLE `topup` DISABLE KEYS */;
INSERT INTO `topup` VALUES ('5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','2f6334a7-3869-486a-a152-2169681cfd5f',500000,500000,1000000,'2021-08-03 20:51:26'),('5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','97749715-4de0-40ac-9aab-2720ec76bb72',500000,0,500000,'2021-08-03 20:51:07');
/*!40000 ALTER TABLE `topup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` varchar(100) NOT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `json` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES ('20957566-f641-4645-bf2a-ee4eef811793','5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','{\"top_up_id\": \"2f6334a7-3869-486a-a152-2169681cfd5f\", \"amount_top_up\": 500000, \"balance_before\": 500000, \"balance_after\": 1000000, \"created_date\": \"2021-08-03T20:51:26\", \"status\": \"SUCCESS\", \"transaction_type\": \"CREDIT\", \"remarks\": \"\", \"user_id\": \"5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e\"}'),('32be69c6-6375-4bde-88d7-d94e529f4ad9','5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','{\"payment_id\": \"ea8405dd-93c4-4ebc-9f1c-85250ebf1e72\", \"amount\": 100000, \"remarks\": \"Pulsa Telkomsel 100k\", \"balance_before\": 1000000, \"balance_after\": 900000, \"created_date\": \"2021-08-03T20:56:38\", \"status\": \"SUCCESS\", \"transaction_type\": \"DEBIT\", \"user_id\": \"5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e\"}'),('639ae27c-9297-4596-99f8-2b3d66dac7aa','5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','{\"transfer_id\": \"0afa865c-c4c6-40f9-95ee-1cc4fa505e81\", \"amount\": 30000, \"remarks\": \"Hadiah Ultah\", \"balance_before\": 900000, \"balance_after\": 870000, \"created_date\": \"2021-08-03T21:04:32\", \"status\": \"SUCCESS\", \"transaction_type\": \"DEBIT\", \"user_id\": \"5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e\"}'),('a0f1e083-35e0-4893-bf99-3647cb101a9d','5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','{\"payment_id\": \"30902446-a242-4217-b6c6-35dcd615fd4d\", \"amount\": 100000, \"remarks\": \"Pulsa Telkomsel 100k\", \"balance_before\": 870000, \"balance_after\": 770000, \"created_date\": \"2021-08-03T21:04:55\", \"status\": \"SUCCESS\", \"transaction_type\": \"DEBIT\", \"user_id\": \"5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e\"}');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer`
--

DROP TABLE IF EXISTS `transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer` (
  `user_id` varchar(100) DEFAULT NULL,
  `transfer_id` varchar(100) NOT NULL,
  `target_user` varchar(100) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  `balance_before` int DEFAULT NULL,
  `balance_after` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  PRIMARY KEY (`transfer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer`
--

LOCK TABLES `transfer` WRITE;
/*!40000 ALTER TABLE `transfer` DISABLE KEYS */;
INSERT INTO `transfer` VALUES ('5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','0afa865c-c4c6-40f9-95ee-1cc4fa505e81','d5f03435-14ec-4f84-b366-311b9741704e',30000,'Hadiah Ultah',900000,870000,'2021-08-03 21:04:32');
/*!40000 ALTER TABLE `transfer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(100) NOT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `pin` varchar(10) DEFAULT NULL,
  `address` text,
  `balance` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('5a2efbba-b9b4-4ce5-9769-00e3b80c2a8e','Guntur','Saputro','0811255501','123456','Jl. Kebon Sirih No. 1',770000,'2021-08-03 20:50:44',NULL),('d5f03435-14ec-4f84-b366-311b9741704e','Rimba','Prayoga','082211967647','123456','Bandung',30000,'2021-08-03 21:03:20',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-03 21:08:28
