-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 13, 2024 at 01:38 PM
-- Server version: 5.7.24
-- PHP Version: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `amal`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(20) NOT NULL,
  `name` text COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `msg` text COLLATE utf8mb4_bin NOT NULL,
  `Date` datetime DEFAULT CURRENT_TIMESTAMP,
  `phone_num` varchar(20) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `msg`, `Date`, `phone_num`) VALUES
(1, 'First-Post', 'email@gmail.com', 'First-Post', '2024-09-18 09:21:05', ''),
(6, 'amal123', 'dddd@gmail.com123', 'Hello', '2024-09-21 08:22:08', '00000000000'),
(10, 'amal123', 'dddd@gmail.com123', 'buyer', '2024-09-22 07:44:37', '00000000000'),
(11, 'amal123', 'dddd@gmail.com123', 'buyer', '2024-09-22 07:46:54', '00000000000'),
(12, 'amal123', 'dddd@gmail.com123', 'yummy', '2024-09-23 08:36:47', '00000000000'),
(13, '', '', '', '2024-09-26 13:47:28', ''),
(14, '', '', '', '2024-09-26 13:47:28', ''),
(15, 'amal', 'bye@gmail.com', 'bye', '2024-10-05 13:02:34', '1234566789632');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(50) NOT NULL,
  `title` text COLLATE utf8mb4_bin NOT NULL,
  `tagline` text COLLATE utf8mb4_bin NOT NULL,
  `slug` varchar(25) COLLATE utf8mb4_bin NOT NULL,
  `content` text COLLATE utf8mb4_bin NOT NULL,
  `img_file` varchar(12) COLLATE utf8mb4_bin NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `tagline`, `slug`, `content`, `img_file`, `date`) VALUES
(2, 'This is Second post', 'coolest post ever', 'Second_post', 'Hey there, welcome to our exclusive space where creativity thrives and words come alive! This is the place where stories are woven, characters are born, and emotions are captured in every sentence. Dive into our world of literary enchantment, where every word is carefully crafted to transport you to new realms and ignite your imagination. Get ready to be swept away by the magic of storytelling and immerse yourself in the power of words!\n\n', 'post-bg.jpg', '2024-10-04 07:54:37'),
(3, 'third title', '\r\nPlease give me the hammer.\r\nPlease give me the red hammer; the blue one is too small.\r\nPlease give me the nails.\r\n', 'third post', 'The definite article is the word the. It limits the meaning of a noun to one particular thing. For example, your friend might ask, “Are you going to the party this weekend?” The definite article tells you that your friend is referring to a specific party that both of you already know about. The definite article can be used with singular, plural, or uncountable nouns. Below are some examples of the definite article, the, used in context:\r\n\r\nPlease give me the hammer.\r\nPlease give me the red hammer; the blue one is too small.\r\nPlease give me the nails.\r\nthird post', '', '2024-10-04 08:18:07'),
(4, 'fourth title', 'fourth tagline', 'fourth post', 'The definite article is the word the. It limits the meaning of a noun to one particular thing. For example, your friend might ask, “Are you going to the party this weekend?” The definite article tells you that your friend is referring to a specific party that both of you already know about. The definite article can be used with singular, plural, or uncountable nouns. Below are some examples of the definite article, the, used in context:\r\n\r\nPlease give me the hammer.\r\nPlease give me the red hammer; the blue one is too small.\r\nPlease give me the nails.\r\n', '', '2024-10-04 08:18:07'),
(5, 'fifth post', 'fifth one', 'fifth slug', 'The definite article is the word the. It limits the meaning of a noun to one particular thing. For example, your friend might ask, “Are you going to the party this weekend?” The definite article tells you that your friend is referring to a specific party that both of you already know about. The definite article can be used with singular, plural, or uncountable nouns. Below are some examples of the definite article, the, used in context:\r\n\r\nPlease give me the hammer.\r\nPlease give me the red hammer; the blue one is too small.\r\nPlease give me the nails.\r\n', '', '2024-10-04 08:19:22'),
(6, 'sixth title', 'sixth one', 'sixth one', 'The definite article is the word the. It limits the meaning of a noun to one particular thing. For example, your friend might ask, “Are you going to the party this weekend?” The definite article tells you that your friend is referring to a specific party that both of you already know about. The definite article can be used with singular, plural, or uncountable nouns. Below are some examples of the definite article, the, used in context:\r\n\r\nPlease give me the hammer.\r\nPlease give me the red hammer; the blue one is too small.\r\nPlease give me the nails.\r\n', '', '2024-10-04 08:19:22'),
(7, 'post blog', 'slug_post_Flask_app', 'for firstly', 'Hey there, welcome to our exclusive space where creativity thrives and words come alive! This is the place where stories are woven, characters are born, and emotions are captured in every sentence. Dive into our world of literary enchantment, where every word is carefully crafted to transport you to new realms and ignite your imagination. Get ready to be swept away by the magic of storytelling and immerse yourself in the power of words!\r\n', '', '2024-10-12 08:33:54');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
