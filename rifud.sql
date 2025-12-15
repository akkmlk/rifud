-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 10, 2025 at 06:32 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rifud`
--

-- --------------------------------------------------------

--
-- Table structure for table `food_waste`
--

CREATE TABLE `food_waste` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` varchar(255) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `price` int NOT NULL,
  `stock` int NOT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `food_waste`
--

INSERT INTO `food_waste` (`id`, `name`, `description`, `foto`, `price`, `stock`, `user_id`) VALUES
(1, 'Sayur Kangkung', 'Sayur kangkung segar sisa dari pasar pagi.', 'kangkung.jpg', 3000, 12, 6),
(2, 'Roti Gandum', 'Roti gandum mendekati tanggal kadaluarsa, masih layak konsumsi.', 'roti_gandum.jpg', 5000, 8, 5),
(3, 'Ayam Ungkep', 'Ayam ungkep dari catering, tidak habis terjual hari ini.', 'ayam_ungkep.jpg', 15000, 5, 4);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int NOT NULL,
  `qty` int NOT NULL,
  `price_total` int NOT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('process','waiting','ready','failed','declined') DEFAULT 'process',
  `user_id` int DEFAULT NULL,
  `food_waste_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `qty`, `price_total`, `transaction_date`, `status`, `user_id`, `food_waste_id`) VALUES
(4, 2, 6000, '2025-12-10 12:51:31', 'process', 6, 1),
(5, 1, 5000, '2025-12-10 12:51:31', 'ready', 5, 2),
(6, 3, 45000, '2025-12-10 12:51:31', 'waiting', 4, 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `longitud` varchar(150) DEFAULT NULL,
  `latitude` varchar(150) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `role` enum('client','resto') DEFAULT 'client'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `phone`, `foto`, `email`, `password`, `address`, `longitud`, `latitude`, `city`, `role`) VALUES
(4, 'Budi Santoso', '081234567890', 'budi.jpg', 'budi@example.com', 'budi123', 'Jl. Merdeka No. 10', '106.827153', '-6.175392', 'Jakarta', 'client'),
(5, 'Siti Aminah', '085612341234', 'siti.png', 'siti@example.com', 'siti123', 'Jl. Melati No. 25', '110.414937', '-7.801194', 'Yogyakarta', 'resto'),
(6, 'Agus Saputra', '082198765432', 'agus.jpeg', 'agus@example.com', 'agus123', 'Jl. Kenanga No. 7', '112.750833', '-7.250445', 'Surabaya', 'client');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `food_waste`
--
ALTER TABLE `food_waste`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id_in_transaction` (`user_id`),
  ADD KEY `fk_food_waste_id` (`food_waste_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `food_waste`
--
ALTER TABLE `food_waste`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `food_waste`
--
ALTER TABLE `food_waste`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_food_waste_id` FOREIGN KEY (`food_waste_id`) REFERENCES `food_waste` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `fk_user_id_in_transaction` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
