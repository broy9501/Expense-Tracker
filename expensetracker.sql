-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 11, 2025 at 12:25 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `expensetracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `expense`
--

CREATE TABLE `expense` (
  `expenseID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `incomeData` date NOT NULL,
  `incomeType` varchar(255) NOT NULL,
  `reference` text NOT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expense`
--

INSERT INTO `expense` (`expenseID`, `title`, `amount`, `incomeData`, `incomeType`, `reference`, `userid`) VALUES
(4, 'test1', '300.00', '2002-11-05', 'op3', 'hjbhhvbdnbsbdwoaoppppp', 2),
(9, 'test2', '200.00', '2025-02-02', 'op2', 'bjbjkjjjjjjjjjjjjjjjjjjjjjjj', 2),
(10, 'test1E', '-100.00', '2025-02-01', 'op4', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaassssssssssssssssss', 2),
(11, 'test2E', '-20.00', '2024-02-03', 'op2', '', 2),
(12, 'test3E', '-50.00', '2022-05-04', 'op1', '', 2),
(13, 'test4E', '-30.00', '2023-02-06', 'op1', '', 2);

-- --------------------------------------------------------

--
-- Table structure for table `totalexpense`
--

CREATE TABLE `totalexpense` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `totalIncome` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `totalexpense`
--

INSERT INTO `totalexpense` (`id`, `userid`, `totalIncome`) VALUES
(2, 2, '300.00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `currencySigns` varchar(10) NOT NULL DEFAULT '£'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `email`, `name`, `password`, `currencySigns`) VALUES
(1, 'test@test.com', 'Test User', 'abc123', '£'),
(2, 'broy9501@gmail.com', 'Bishal Roy', '$2b$12$pcRc5lEB6Sfss6qbL9CIn.bJKQN0K7foQucuz0SQTToypdqefegMG', '₹');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `expense`
--
ALTER TABLE `expense`
  ADD PRIMARY KEY (`expenseID`),
  ADD KEY `fk_userid` (`userid`);

--
-- Indexes for table `totalexpense`
--
ALTER TABLE `totalexpense`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `expense`
--
ALTER TABLE `expense`
  MODIFY `expenseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `totalexpense`
--
ALTER TABLE `totalexpense`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `expense`
--
ALTER TABLE `expense`
  ADD CONSTRAINT `fk_userid` FOREIGN KEY (`userid`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `totalexpense`
--
ALTER TABLE `totalexpense`
  ADD CONSTRAINT `totalexpense_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
