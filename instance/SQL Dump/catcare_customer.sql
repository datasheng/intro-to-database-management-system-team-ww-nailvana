CREATE DATABASE  IF NOT EXISTS `catcare` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `catcare`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: catcare
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(100) DEFAULT NULL,
  `Password` varchar(150) DEFAULT NULL,
  `Name` varchar(32) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Email` varchar(64) DEFAULT NULL,
  `Number` bigint DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'rand2002','pbkdf2:sha256:600000$cAPH9Nw2qrF89AVn$58600fc2a3ee8739c5e6c1c09fdd60fb148066817313f8b2a9df8f849f229138','Random User',NULL,'random@gmail.com',NULL),(2,'deadpool2016','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Caleb Reynolds',NULL,'cReynolds16@gmail.com',NULL),(3,'moonmaiden','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Luna Thompson',NULL,'laluna@gmail.com',NULL),(4,'friendlyghost','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Jasper Patel',NULL,'metalpetal@gmail.com',NULL),(5,'magicmaya','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Maya Mitchell',NULL,'magicmaya@gmail.com',NULL),(6,'Felix2002','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Felix Garcia',NULL,'felixg@gmail.com',NULL),(7,'claroquesi','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Clara Nguyen',NULL,'ofcourse1999@gmail.com',NULL),(8,'PheonixW','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Owen Wright',NULL,'acelawyer@gmail.com',NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-25 17:06:37
