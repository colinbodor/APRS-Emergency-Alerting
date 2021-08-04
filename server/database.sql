-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 04, 2021 at 10:45 AM
-- Server version: 8.0.26-0ubuntu0.20.04.2
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aprs`
--

-- --------------------------------------------------------

--
-- Table structure for table `abfire`
--

CREATE TABLE `abfire` (
  `id` int NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `yesterday_datetime` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fire_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `year` varchar(255) DEFAULT NULL,
  `fire_num_yr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `assessment_datetime` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fire_location_latitude` float DEFAULT NULL,
  `fire_location_longitude` float DEFAULT NULL,
  `general_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cr_id` varchar(255) DEFAULT NULL,
  `id1` varchar(255) DEFAULT NULL,
  `id2` varchar(255) DEFAULT NULL,
  `percent_contained` varchar(255) DEFAULT NULL,
  `fire_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `area_burned` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `no_of_wfu` varchar(255) DEFAULT NULL,
  `no_of_manpower` varchar(255) DEFAULT NULL,
  `no_of_ag` varchar(255) DEFAULT NULL,
  `no_of_aircraft` varchar(255) DEFAULT NULL,
  `no_of_equipment` varchar(255) DEFAULT NULL,
  `no_of_ac_rw_light` varchar(255) DEFAULT NULL,
  `no_of_ac_rw_medium` varchar(255) DEFAULT NULL,
  `no_of_ac_rw_inter` varchar(255) DEFAULT NULL,
  `no_of_veq_truck` varchar(255) DEFAULT NULL,
  `no_of_veq_truck_wt` varchar(255) DEFAULT NULL,
  `no_of_veq_skidder` varchar(255) DEFAULT NULL,
  `no_of_veq_bus` varchar(255) DEFAULT NULL,
  `no_of_veq_dozer` varchar(255) DEFAULT NULL,
  `no_of_fl_eq_pump` varchar(255) DEFAULT NULL,
  `cr_group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `report_creation_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `eco_zone_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `modified_action_flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `web_general_cause` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fire_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `group_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `group_sort_1` varchar(255) DEFAULT NULL,
  `fire_complex_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fire_complex_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fire_complex_year` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `abroads`
--

CREATE TABLE `abroads` (
  `id` int NOT NULL,
  `abid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `organization` varchar(255) NOT NULL,
  `roadwayname` varchar(255) NOT NULL,
  `directionoftravel` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `reported` varchar(255) NOT NULL,
  `lastupdated` varchar(255) NOT NULL,
  `startdate` varchar(255) NOT NULL,
  `plannedenddate` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `lanesaffected` varchar(255) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `latitudesecondary` varchar(255) NOT NULL,
  `longitudesecondary` varchar(255) NOT NULL,
  `eventtype` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `alerts`
--

CREATE TABLE `alerts` (
  `id` int NOT NULL,
  `feed` varchar(255) NOT NULL,
  `title` text NOT NULL,
  `link` text NOT NULL,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `aprs_log`
--

CREATE TABLE `aprs_log` (
  `id` int NOT NULL,
  `timestamp` datetime NOT NULL,
  `direction` varchar(15) NOT NULL,
  `callsign` varchar(15) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fedfire`
--

CREATE TABLE `fedfire` (
  `id` int NOT NULL,
  `agency` varchar(255) NOT NULL,
  `firename` varchar(255) NOT NULL,
  `lat` float NOT NULL,
  `lon` float NOT NULL,
  `startdate` varchar(255) NOT NULL,
  `hectares` varchar(255) NOT NULL,
  `stage_of_control` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fetch_log`
--

CREATE TABLE `fetch_log` (
  `id` int NOT NULL,
  `process` varchar(255) NOT NULL,
  `events` int NOT NULL,
  `rundate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `heartbeat`
--

CREATE TABLE `heartbeat` (
  `id` int NOT NULL,
  `task` varchar(255) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `location_data`
--

CREATE TABLE `location_data` (
  `id` int NOT NULL,
  `land_water` varchar(10) NOT NULL,
  `prov_water_code` varchar(255) NOT NULL,
  `loc_type` varchar(10) NOT NULL,
  `clc` int NOT NULL,
  `loc_name_en` text NOT NULL,
  `loc_name_fr` text NOT NULL,
  `loc_name_upper_en` text NOT NULL,
  `loc_name_upper_fr` text NOT NULL,
  `tz_code` text NOT NULL,
  `tz_identified` text NOT NULL,
  `adm_prog` varchar(255) NOT NULL,
  `banner_loc_code` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `naads`
--

CREATE TABLE `naads` (
  `id` int NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `identifier` varchar(255) NOT NULL,
  `language` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `event` varchar(255) NOT NULL,
  `responsetype` varchar(255) NOT NULL,
  `urgency` varchar(255) NOT NULL,
  `severity` varchar(255) NOT NULL,
  `certainty` varchar(255) NOT NULL,
  `audience` varchar(255) NOT NULL,
  `sendername` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `headline` text NOT NULL,
  `description` text NOT NULL,
  `instruction` text NOT NULL,
  `effective_gmt` datetime NOT NULL,
  `expires_gmt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `naads_area`
--

CREATE TABLE `naads_area` (
  `id` int NOT NULL,
  `identifier` varchar(255) NOT NULL,
  `language` varchar(10) NOT NULL,
  `areadesc` text NOT NULL,
  `polygon` text NOT NULL,
  `clc` varchar(255) NOT NULL,
  `capcp_loc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `naads_xml`
--

CREATE TABLE `naads_xml` (
  `id` int NOT NULL,
  `identifier` varchar(255) NOT NULL,
  `xml` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `abfire`
--
ALTER TABLE `abfire`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `abroads`
--
ALTER TABLE `abroads`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `alerts`
--
ALTER TABLE `alerts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `aprs_log`
--
ALTER TABLE `aprs_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fedfire`
--
ALTER TABLE `fedfire`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fetch_log`
--
ALTER TABLE `fetch_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `heartbeat`
--
ALTER TABLE `heartbeat`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location_data`
--
ALTER TABLE `location_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `naads`
--
ALTER TABLE `naads`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `naads_area`
--
ALTER TABLE `naads_area`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `naads_xml`
--
ALTER TABLE `naads_xml`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `abfire`
--
ALTER TABLE `abfire`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `abroads`
--
ALTER TABLE `abroads`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `alerts`
--
ALTER TABLE `alerts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `aprs_log`
--
ALTER TABLE `aprs_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fedfire`
--
ALTER TABLE `fedfire`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fetch_log`
--
ALTER TABLE `fetch_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `heartbeat`
--
ALTER TABLE `heartbeat`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `location_data`
--
ALTER TABLE `location_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `naads`
--
ALTER TABLE `naads`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `naads_area`
--
ALTER TABLE `naads_area`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `naads_xml`
--
ALTER TABLE `naads_xml`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
