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
-- Dumping routines for database 'catcare'
--
/*!50003 DROP PROCEDURE IF EXISTS `create_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_tables`()
BEGIN
    CREATE TABLE Provider(
		ProviderID INT PRIMARY KEY,
		Username VARCHAR(100),
		Password VARCHAR(150),
		Name VARCHAR(32),
		Address VARCHAR(255),
		Email VARCHAR(64),
		Number BIGINT(10),
		Industry VARCHAR(64),
		Specialization VARCHAR(64),
		Company VARCHAR(64),
		PriceRate INT,
		Rating INT,
		ScheduleID INT,
		FOREIGN KEY (ScheduleID) REFERENCES ProviderSchedule(ScheduleID)
	);
    
	CREATE TABLE Customer(
		CustomerID INT PRIMARY KEY,
		Username VARCHAR(100),
		Password VARCHAR(150),
		Name VARCHAR(32),
		Address VARCHAR(255),
		Email VARCHAR(64),
		Number BIGINT(10)
	);


	CREATE TABLE Pet(
		PetID INT PRIMARY KEY,
		Name VARCHAR(64),
		Age INT,
		Species VARCHAR(3),
		Breed VARCHAR(32),
		CustomerID INT,
		FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
	);

	CREATE TABLE ProviderSchedule(
		ScheduleID INT NOT NULL PRIMARY KEY,
		Day DATE,
		StartTime DATETIME,
		EndTime DATETIME
	);
    
	CREATE TABLE PetAppointment(
		AppointmentID INT PRIMARY KEY,
		ProviderID INT,
		PetID INT,
		FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID),
		FOREIGN KEY (PetID) REFERENCES Pet(PetID),
		Status VARCHAR(32),
		BorrowDate DATETIME,
		ReturnDate DATETIME
	);

	CREATE TABLE NailAppointment(
		AppointmentID INT PRIMARY KEY,
		ProviderID INT,
		CustomerID INT,
		FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID),
		FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
		Status VARCHAR(32),
		BorrowDate DATETIME,
		ReturnDate DATETIME
	);
    
    CREATE TABLE Review (
		ReviewID INT PRIMARY KEY,
		ProviderID INT NOT NULL,
		ServiceType VARCHAR(20), 
		Rating INT, 
		Comment TEXT, 
		FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID)
	);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `drop_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `drop_tables`()
BEGIN
	DROP TABLE review;
	DROP TABLE nailappointment;
	DROP TABLE petappointment;
	DROP TABLE pet;
	DROP TABLE customer;
	DROP TABLE provider;
	DROP TABLE providerschedule;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_dummy` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_dummy`()
BEGIN
	INSERT INTO Customer(Username, Password, Name, Email) VALUES
    ("deadpool2016", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Caleb Reynolds", "cReynolds16@gmail.com"),
    ("moonmaiden", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Luna Thompson", "laluna@gmail.com"),
    ("friendlyghost", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Jasper Patel", "metalpetal@gmail.com"),
    ("magicmaya", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Maya Mitchell", "magicmaya@gmail.com"),
    ("Felix2002", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Felix Garcia", "felixg@gmail.com"),
    ("claroquesi", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Clara Nguyen", "ofcourse1999@gmail.com"),
    ("PheonixW", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Owen Wright", "acelawyer@gmail.com");
    
    INSERT INTO Provider(Username, Password, Name, Email) VALUES
    ("HEvans1999", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Harper Evans", "hevans@yahoo.com"),
    ("LiamC2001", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Liam Campbell", "liamC2001@gmail.com"),
    ("ZoeArt", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342","Zoe Ramirez", "zoeart@gmail.com"),
    ("MarkerArtist", "pbkdf2:sha256:600000$LD2qx1Qaz8mGYq22$499a01423900ecd148cc2ccdbd8fff387e9dbe2cf429761d5ccbadeee997f342" ,"Isaac Clarke", "markerart@yahoo.com");
    
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-25 17:06:38
