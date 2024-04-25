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
-- Table structure for table `provider`
--

DROP TABLE IF EXISTS `provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provider` (
  `ProviderID` int NOT NULL AUTO_INCREMENT,
  `ScheduleID` int DEFAULT NULL,
  `Username` varchar(100) DEFAULT NULL,
  `Password` varchar(150) DEFAULT NULL,
  `Name` varchar(32) DEFAULT NULL,
  `Industry` varchar(64) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Email` varchar(64) DEFAULT NULL,
  `Number` bigint DEFAULT NULL,
  `Rating` int DEFAULT NULL,
  `PriceRate` int DEFAULT NULL,
  `Specialization` varchar(64) DEFAULT NULL,
  `Company` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`ProviderID`),
  KEY `ScheduleID` (`ScheduleID`),
  CONSTRAINT `provider_ibfk_1` FOREIGN KEY (`ScheduleID`) REFERENCES `providerschedule` (`ScheduleID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provider`
--

LOCK TABLES `provider` WRITE;
/*!40000 ALTER TABLE `provider` DISABLE KEYS */;
INSERT INTO `provider` VALUES (1,NULL,'lisared95','pbkdf2:sha256:600000$HAZOv68UBODknO3g$f3e711612e415f43cdf2981853e3e61da61c9d393fd71eaa034ea057fc7fe2d6','Lisa Red',NULL,NULL,'lisared95@gmail.com',NULL,NULL,NULL,NULL,NULL),(2,NULL,'HEvans1999','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Harper Evans',NULL,NULL,'hevans@yahoo.com',NULL,NULL,NULL,NULL,NULL),(3,NULL,'LiamC2001','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Liam Campbell',NULL,NULL,'liamC2001@gmail.com',NULL,NULL,NULL,NULL,NULL),(4,NULL,'ZoeArt','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Zoe Ramirez',NULL,NULL,'zoeart@gmail.com',NULL,NULL,NULL,NULL,NULL),(5,NULL,'MarkerArtist','pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342','Isaac Clarke',NULL,NULL,'markerart@yahoo.com',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `provider` ENABLE KEYS */;
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
