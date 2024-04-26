-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: mechanic_work
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `APPOINTMENTS`
--

DROP TABLE IF EXISTS `APPOINTMENTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APPOINTMENTS` (
  `AppNum` int NOT NULL AUTO_INCREMENT,
  `AppDate` date NOT NULL,
  `VIN` varchar(17) NOT NULL,
  `CustID` int NOT NULL,
  PRIMARY KEY (`AppNum`),
  KEY `VIN` (`VIN`),
  KEY `CustID` (`CustID`),
  CONSTRAINT `APPOINTMENTS_ibfk_1` FOREIGN KEY (`VIN`) REFERENCES `CARS` (`VIN`),
  CONSTRAINT `APPOINTMENTS_ibfk_2` FOREIGN KEY (`CustID`) REFERENCES `CUSTOMERS` (`CustID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APPOINTMENTS`
--

LOCK TABLES `APPOINTMENTS` WRITE;
/*!40000 ALTER TABLE `APPOINTMENTS` DISABLE KEYS */;
INSERT INTO `APPOINTMENTS` VALUES (1,'2024-05-23','2FTRX18W1XCA01324',1111),(2,'2024-04-30','123123213123',1111);
/*!40000 ALTER TABLE `APPOINTMENTS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CARS`
--

DROP TABLE IF EXISTS `CARS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CARS` (
  `VIN` varchar(17) NOT NULL,
  `Make` varchar(255) NOT NULL,
  `Model` varchar(255) NOT NULL,
  `Year` int NOT NULL,
  `CustID` int NOT NULL,
  PRIMARY KEY (`VIN`),
  KEY `CustID` (`CustID`),
  CONSTRAINT `CARS_ibfk_1` FOREIGN KEY (`CustID`) REFERENCES `CUSTOMERS` (`CustID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CARS`
--

LOCK TABLES `CARS` WRITE;
/*!40000 ALTER TABLE `CARS` DISABLE KEYS */;
INSERT INTO `CARS` VALUES ('123123213123','Jeep','Grand Cherokee',2003,1111),('2FTRX18W1XCA01324','Ford','F150',1999,1111);
/*!40000 ALTER TABLE `CARS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CUSTOMERS`
--

DROP TABLE IF EXISTS `CUSTOMERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CUSTOMERS` (
  `CustID` int NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `FirstName` varchar(255) NOT NULL,
  `PhoneNumber` varchar(11) NOT NULL,
  PRIMARY KEY (`CustID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMERS`
--

LOCK TABLES `CUSTOMERS` WRITE;
/*!40000 ALTER TABLE `CUSTOMERS` DISABLE KEYS */;
INSERT INTO `CUSTOMERS` VALUES (1111,'Johnson','Harold','6365555555');
/*!40000 ALTER TABLE `CUSTOMERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `INVOICE`
--

DROP TABLE IF EXISTS `INVOICE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `INVOICE` (
  `InvoiceNum` int NOT NULL AUTO_INCREMENT,
  `PartsCost` float NOT NULL,
  `LaborCost` float NOT NULL,
  `TechID` int NOT NULL,
  `VIN` varchar(17) NOT NULL,
  `RepairNum` int NOT NULL,
  `Paid` bit(1) NOT NULL,
  PRIMARY KEY (`InvoiceNum`),
  KEY `VIN` (`VIN`),
  KEY `TechID` (`TechID`),
  CONSTRAINT `INVOICE_ibfk_1` FOREIGN KEY (`VIN`) REFERENCES `CARS` (`VIN`),
  CONSTRAINT `INVOICE_ibfk_2` FOREIGN KEY (`TechID`) REFERENCES `TECHNICIAN` (`TechID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `INVOICE`
--

LOCK TABLES `INVOICE` WRITE;
/*!40000 ALTER TABLE `INVOICE` DISABLE KEYS */;
INSERT INTO `INVOICE` VALUES (1,1950.5,366.43,71502,'2FTRX18W1XCA01324',1,_binary '');
/*!40000 ALTER TABLE `INVOICE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LOGIN`
--

DROP TABLE IF EXISTS `LOGIN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LOGIN` (
  `TechID` int NOT NULL,
  `Password` binary(32) NOT NULL,
  `salt` binary(10) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`TechID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LOGIN`
--

LOCK TABLES `LOGIN` WRITE;
/*!40000 ALTER TABLE `LOGIN` DISABLE KEYS */;
INSERT INTO `LOGIN` VALUES (123,_binary 'Ωì_wt	c‰±Ç\Ï\ﬂMVÖÜ5€≤I\Ã`\Œ\Î\◊\Ì∑\ÏÑ',_binary 'nØb¢Kö:√í±','email@gmail.com'),(71502,_binary 'h¶PaàìH	ƒ∂^\Í´=Jç¯\Z\÷¡¢\Ì= 9•y©vI\È',_binary 'l\ˆ\“∆ú\Â\Ë-ú\’','tkeith1@ccis.edu');
/*!40000 ALTER TABLE `LOGIN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REPAIRS`
--

DROP TABLE IF EXISTS `REPAIRS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REPAIRS` (
  `RepairNum` int NOT NULL AUTO_INCREMENT,
  `VIN` varchar(17) NOT NULL,
  `TechID` int NOT NULL,
  `InMiles` float DEFAULT NULL,
  `OutMiles` float DEFAULT NULL,
  `Cost` float NOT NULL,
  PRIMARY KEY (`RepairNum`),
  KEY `TechID` (`TechID`),
  KEY `VIN` (`VIN`),
  CONSTRAINT `REPAIRS_ibfk_1` FOREIGN KEY (`TechID`) REFERENCES `TECHNICIAN` (`TechID`),
  CONSTRAINT `REPAIRS_ibfk_2` FOREIGN KEY (`VIN`) REFERENCES `CARS` (`VIN`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REPAIRS`
--

LOCK TABLES `REPAIRS` WRITE;
/*!40000 ALTER TABLE `REPAIRS` DISABLE KEYS */;
INSERT INTO `REPAIRS` VALUES (1,'2FTRX18W1XCA01324',71502,165000,165026,2316.93);
/*!40000 ALTER TABLE `REPAIRS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SHOP`
--

DROP TABLE IF EXISTS `SHOP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SHOP` (
  `Name` varchar(25) NOT NULL,
  `Address` varchar(25) NOT NULL,
  `PhoneNumber` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SHOP`
--

LOCK TABLES `SHOP` WRITE;
/*!40000 ALTER TABLE `SHOP` DISABLE KEYS */;
INSERT INTO `SHOP` VALUES ('CarShop5','123 Street Columbia MO','5731234567');
/*!40000 ALTER TABLE `SHOP` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TASKS`
--

DROP TABLE IF EXISTS `TASKS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TASKS` (
  `TaskID` int NOT NULL AUTO_INCREMENT,
  `Descr` mediumtext NOT NULL,
  `RepairNum` int NOT NULL,
  PRIMARY KEY (`TaskID`),
  KEY `RepairNum` (`RepairNum`),
  CONSTRAINT `TASKS_ibfk_1` FOREIGN KEY (`RepairNum`) REFERENCES `REPAIRS` (`RepairNum`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TASKS`
--

LOCK TABLES `TASKS` WRITE;
/*!40000 ALTER TABLE `TASKS` DISABLE KEYS */;
INSERT INTO `TASKS` VALUES (1,'Remove and Replace Front Driver Side CV Axle',1);
/*!40000 ALTER TABLE `TASKS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TECHNICIAN`
--

DROP TABLE IF EXISTS `TECHNICIAN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TECHNICIAN` (
  `TechID` int NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `Payrate` decimal(15,2) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `FirstName` varchar(255) NOT NULL,
  PRIMARY KEY (`TechID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TECHNICIAN`
--

LOCK TABLES `TECHNICIAN` WRITE;
/*!40000 ALTER TABLE `TECHNICIAN` DISABLE KEYS */;
INSERT INTO `TECHNICIAN` VALUES (123,'Stevebob',NULL,'2024-04-17','Susie'),(71502,'Keith',20.50,'2002-07-15','Tristan');
/*!40000 ALTER TABLE `TECHNICIAN` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-26 16:16:13
