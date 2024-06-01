-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 19, 2020 at 08:20 AM
-- Server version: 10.4.11-MariaDB
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
-- Database: `art`
--

-- --------------------------------------------------------

--
-- Table structure for table `addart`
--

CREATE TABLE `addart` (
  `id` int(200) NOT NULL,
  `sellername` varchar(200) NOT NULL,
  `artistname` varchar(200) NOT NULL,
  `artworktitle` varchar(200) NOT NULL,
  `category` varchar(200) NOT NULL,
  `year` varchar(200) NOT NULL,
  `height` int(255) NOT NULL,
  `width` int(255) NOT NULL,
  `sign` varchar(200) NOT NULL,
  `certificate` varchar(200) NOT NULL,
  `acquire` varchar(200) NOT NULL,
  `city` varchar(200) NOT NULL,
  `minprice` int(200) NOT NULL,
  `date` varchar(200) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `file` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `addart`
--

INSERT INTO `addart` (`id`, `sellername`, `artistname`, `artworktitle`, `category`, `year`, `height`, `width`, `sign`, `certificate`, `acquire`, `city`, `minprice`, `date`, `phone`, `file`) VALUES
(1, 'Vishal', 'Vishal', 'Camila', 'Painting', '2020', 200, 120, 'Yes', 'No', 'Belgaum', 'Belgaum', 3000, '2020-10-15 12:00', '2147483647', 'camila.jpg'),
(2, 'Pratiksha', 'Pratiksha', 'Flower Vase', 'Photography', '2020', 100, 80, 'Yes', 'No', 'Belgaum', 'Belgaum', 2000, '2020-10-20 12:00', '2147483647', '59.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(200) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `phone` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `phone`, `password`) VALUES
(1, 'admin', 'admin@gmail.com', '8073220941', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `bidding`
--

CREATE TABLE `bidding` (
  `id` int(200) NOT NULL,
  `name` varchar(200) NOT NULL,
  `bidamount` varchar(200) NOT NULL,
  `paint_id` int(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bidding`
--

INSERT INTO `bidding` (`id`, `name`, `bidamount`, `paint_id`) VALUES
(1, 'Yash Potdar', '4000', 1),
(2, 'Yash Potdar', '3000', 2),
(3, 'Soumya Chaugala', '5000', 1),
(4, 'Nikhil Kukude', '6000', 1),
(5, 'Nikhil Kukude', '4000', 2),
(10, 'Vishal Jagamani', '7000', 1);

-- --------------------------------------------------------

--
-- Table structure for table `finalbid`
--

CREATE TABLE `finalbid` (
  `id` int(200) NOT NULL,
  `seller` varchar(200) NOT NULL,
  `contact` varchar(200) NOT NULL,
  `artistname` varchar(200) NOT NULL,
  `arttitle` varchar(200) NOT NULL,
  `finalprice` varchar(200) NOT NULL,
  `winner` varchar(200) NOT NULL,
  `artimage` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `finalbid`
--

INSERT INTO `finalbid` (`id`, `seller`, `contact`, `artistname`, `arttitle`, `finalprice`, `winner`, `artimage`) VALUES
(5, 'Vishal', '8073220941', 'Vishal', 'camila', '6000', 'Yash Potdar', 'camila_cabello_vector_portrait_by_danielta2669_dc061bp.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(200) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `category` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `email`, `phone`, `address`, `password`, `category`) VALUES
(1, 'Vishal Jagamani', 'vishalgj10@gmail.com', '8073220941', 'Angol, Belgaum', '$5$rounds=535000$m6kBLP4XV2zfcHxF$3EtkbIkFtJbNr1Akx28O.KYE1cLQ9fLBDqAeERq4Zn1', 'Seller'),
(2, 'Pratiksha Desai', 'pratiksha@gmail.com', '7337853168', 'Halga, Belgaum', '$5$rounds=535000$Za4J.A.v4/TP6fuk$PkETBS66VpCuo9h5I3RsfdMbcyh4yYBz7z.uiTe2xv3', 'Seller'),
(3, 'Yash P', 'yash10@gmail.com', '9019841191', 'Old Belgaum, belgaum', '$5$rounds=535000$PdfGyyJU8tdz5RFk$YLeoJU0ut6tUbJHBVDuiRhSgsYS.dr7mjwKtM9FRsl/', 'Buyer'),
(4, 'Soumya Chaugala', 'soumya@gmail.com', '9019859499', 'Alarwad, Belgaum', '$5$rounds=535000$8ReJU0qvXvLhvKIP$GDBW9JVMjDn8wtkvbuMJ8JEqdj2k5EfEahnUZ6wgNl1', 'Buyer'),
(5, 'Severin Dsouza', 'severin@gmail.com', '7083968335', 'Damane, Belgaum', '$5$rounds=535000$.vnFEucocYn/Gmrf$94S2DN2tEgN0MnWCa2TnyFBdPaLhlir2h0s/uU6rmu7', 'Buyer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `addart`
--
ALTER TABLE `addart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bidding`
--
ALTER TABLE `bidding`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `finalbid`
--
ALTER TABLE `finalbid`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `register`
--
ALTER TABLE `register`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `addart`
--
ALTER TABLE `addart`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bidding`
--
ALTER TABLE `bidding`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `finalbid`
--
ALTER TABLE `finalbid`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `register`
--
ALTER TABLE `register`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
