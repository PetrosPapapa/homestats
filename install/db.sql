SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


--
-- Table structure for table `energy`
--

CREATE TABLE `energy` (
  `address` varchar(32) NOT NULL DEFAULT 'Home',
  `date` date NOT NULL,
  `electricity` int(10) UNSIGNED NOT NULL,
  `gas` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(10) UNSIGNED NOT NULL,
  `Date` date NOT NULL,
  `Type` varchar(12) DEFAULT NULL,
  `Description` text NOT NULL,
  `Value` float NOT NULL,
  `Balance` float DEFAULT NULL,
  `Account Name` varchar(35) NOT NULL,
  `Account Number` varchar(25) NOT NULL,
  `Category` varchar(12) NOT NULL DEFAULT 'UNKNOWN'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for table `energy`
--
ALTER TABLE `energy`
  ADD PRIMARY KEY (`address`,`date`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `Category` (`Category`);

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
