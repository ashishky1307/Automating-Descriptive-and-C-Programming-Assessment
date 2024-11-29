-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 24, 2024 at 06:44 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `exam_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `answers`
--

CREATE TABLE `answers` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  `answer` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `evaluations`
--

CREATE TABLE `evaluations` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  `similarity` float DEFAULT NULL,
  `predicted_marks` float DEFAULT NULL,
  `total_marks` float DEFAULT NULL,
  `grammar_mistakes` int(11) DEFAULT NULL,
  `summary` text DEFAULT NULL,
  `word_count` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evaluations`
--

INSERT INTO `evaluations` (`id`, `student_id`, `question_id`, `similarity`, `predicted_marks`, `total_marks`, `grammar_mistakes`, `summary`, `word_count`) VALUES
(128, 1, 6, 100, 10, NULL, 0, NULL, 29),
(137, 1, 20, 62.62, 10, NULL, 3, 'Error generating summary.', 11),
(141, 1, 7, 3.33, 0, NULL, 1, NULL, 1),
(142, 2, 8, 60.74, 10, NULL, 2, 'Error generating summary.', 64),
(143, 2, 19, 74.66, 10, NULL, 0, 'Error generating summary.', 20),
(144, 2, 20, 16.34, 0, NULL, 0, NULL, 0),
(145, 2, 6, 75.54, 10, NULL, 0, 'Error generating summary.', 33),
(146, 2, 7, 81.96, 10, NULL, 0, 'Error generating summary.', 12);

-- --------------------------------------------------------

--
-- Table structure for table `evaluators`
--

CREATE TABLE `evaluators` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evaluators`
--

INSERT INTO `evaluators` (`id`, `name`, `email`, `password`, `created_at`) VALUES
(1, 'komal', 'p@gmail', 'pass123', '2024-09-17 13:52:59');

-- --------------------------------------------------------

--
-- Table structure for table `question`
--

CREATE TABLE `question` (
  `id` int(11) NOT NULL,
  `question_text` text NOT NULL,
  `model_answer` text NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `question`
--

INSERT INTO `question` (`id`, `question_text`, `model_answer`, `created_by`, `created_at`) VALUES
(1, 'abc', 'kjsdlfkj', NULL, '2024-09-17 14:54:35');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(11) NOT NULL,
  `question_text` text NOT NULL,
  `model_answer` text NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question_text`, `model_answer`, `created_by`, `created_at`) VALUES
(6, 'What does static variable mean?', 'Static variables are the variables which retain their values between the function calls. They are initialized only once their scope is within the function in which they are defined.', 1, '2024-09-17 13:46:12'),
(7, 'What is a pointer?', 'Pointers are variables which stores the address of another variable. That variable may be a\r\nscalar (including another pointer), or an aggregate (array or structure). The pointed-to object may\r\nbe part of a larger object, such as a field of a structure or an element in an array.', 1, '2024-09-17 13:46:52'),
(8, 'What is recursion?', 'A recursion function is one which calls itself either directly or indirectly it must halt at a definite point to avoid infinite recursion.', 1, '2024-09-17 13:47:34'),
(19, 'What does static variable mean?\r\n', '\"Static variables are the variables which retain their values between the function calls. They\r\nare initialized only once their scope is within the function in which they are defined.\"\r\n', 1, '2024-09-21 09:57:45'),
(20, 'What is a pointer?\r\n', '\"Pointers are variables which stores the address of another variable. That variable may be a\nscalar (including another pointer), or an aggregate (array or structure). The pointed-to object may\nbe part of a larger object, such as a field of a structure or an element in an array.\"\n', 1, '2024-09-21 09:58:05'),
(21, 'Where is the auto variables stored?\r\n', '\"Auto variables can be stored anywhere, so long as recursion works. Practically, they������������������re\r\nstored on\r\nthe stack. It is not necessary that always a stack exist. You could theoretically allocate function\r\ninvocation record\"\r\n', 1, '2024-09-21 09:58:29'),
(22, 'n', 'm', 1, '2024-09-25 14:47:30'),
(23, 'what is c lang?', 'C lang refers to the programming language C, which was originally developed by Dennis Ritchie in the early 1970s at Bell Labs. C is a general-purpose, procedural programming language known for its efficiency, flexibility, and direct control over hardware. It has influenced many other programming languages and is widely used in system software, embedded systems, and application software where performance and efficiency are crucial. C is known for its powerful features like pointers, structured programming, and a rich standard library.', 1, '2024-11-14 12:16:38'),
(24, 'kj', 'lkjlkj', 1, '2024-11-14 18:23:07'),
(25, 'what is variable in c?', 'variable is container which holds the specific type of the data such as integer , float, character. ', 1, '2024-11-15 05:11:07'),
(26, 'what is varible ?', 'varible ', 1, '2024-11-15 06:56:41'),
(27, 'what is variable?', 'varible is container to stored a data in a program', 1, '2024-11-15 07:53:19');

-- --------------------------------------------------------

--
-- Table structure for table `question_paper`
--

CREATE TABLE `question_paper` (
  `id` int(11) NOT NULL,
  `paper_name` varchar(255) NOT NULL,
  `evaluator_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `question_paper`
--

INSERT INTO `question_paper` (`id`, `paper_name`, `evaluator_id`, `created_at`) VALUES
(80, 'paper 1', 1, '2024-11-15 00:21:57'),
(81, 'paper 2', 1, '2024-11-15 01:27:20'),
(82, 'paper 3', 1, '2024-11-15 02:23:54');

-- --------------------------------------------------------

--
-- Table structure for table `question_paper_question`
--

CREATE TABLE `question_paper_question` (
  `id` int(11) NOT NULL,
  `question_paper_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `question_paper_question`
--

INSERT INTO `question_paper_question` (`id`, `question_paper_id`, `question_id`) VALUES
(15, 80, 6),
(16, 80, 7),
(17, 80, 8),
(18, 81, 8),
(19, 81, 19),
(20, 81, 20),
(21, 82, 8),
(22, 82, 19),
(23, 82, 20);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `final_score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `name`, `final_score`) VALUES
(1, 'komal', 13),
(2, 'student2', 20);

-- --------------------------------------------------------

--
-- Table structure for table `student_answer`
--

CREATE TABLE `student_answer` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `answer_text` text NOT NULL,
  `submitted_at` datetime DEFAULT current_timestamp(),
  `model_ans` text DEFAULT NULL,
  `marks` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_answer`
--

INSERT INTO `student_answer` (`id`, `student_id`, `question_id`, `answer_text`, `submitted_at`, `model_ans`, `marks`) VALUES
(65, 1, 6, 'Static variables are the variables which retain their values between the function calls. They are initialized only once their scope is within the function in which they are defined.', '2024-11-15 05:53:30', NULL, NULL),
(66, 1, 7, 'sfsdf', '2024-11-15 05:53:30', NULL, NULL),
(70, 1, 20, 'pointer is used to store a memeroy add of a varible.', '2024-11-15 06:58:36', NULL, NULL),
(74, 2, 8, 'Recursion is a programming technique where a function calls itself directly or indirectly to solve a problem. It involves breaking down a problem into smaller, similar subproblems and solving each subproblem until a base condition is met, which stops the recursive calls. Recursion is commonly used in algorithms where the solution to a problem depends on solutions to smaller instances of the same problem.\r\n\r\n', '2024-11-15 07:54:49', NULL, NULL),
(75, 2, 19, 'A static variable is a variable that retains its value between function calls or across different instances of a class', '2024-11-15 07:54:49', NULL, NULL),
(76, 2, 20, '', '2024-11-15 07:54:49', NULL, NULL),
(77, 2, 6, 'A static variable in programming refers to a variable that retains its value between function calls. It\'s usually associated with a class or a function and remains in memory throughout the program\'s execution.\r\n\r\n', '2024-11-19 11:35:23', NULL, NULL),
(78, 2, 7, 'A pointer is a variable that stores the address of another variable.', '2024-11-19 11:35:23', NULL, NULL),
(79, 2, 8, 'Recursion in programming refers to a technique where a function calls itself directly or indirectly in order to solve a problem. This technique is especially useful for tasks that can be broken down into smaller, similar subproblems. ', '2024-11-19 11:35:23', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `answers`
--
ALTER TABLE `answers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `question_id` (`question_id`);

--
-- Indexes for table `evaluations`
--
ALTER TABLE `evaluations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_entry` (`student_id`,`question_id`),
  ADD KEY `evaluations_ibfk_2` (`question_id`);

--
-- Indexes for table `evaluators`
--
ALTER TABLE `evaluators`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `question`
--
ALTER TABLE `question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_evaluator` (`created_by`);

--
-- Indexes for table `question_paper`
--
ALTER TABLE `question_paper`
  ADD PRIMARY KEY (`id`),
  ADD KEY `evaluator_id` (`evaluator_id`);

--
-- Indexes for table `question_paper_question`
--
ALTER TABLE `question_paper_question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question_paper_id` (`question_paper_id`),
  ADD KEY `question_id` (`question_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student_answer`
--
ALTER TABLE `student_answer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_student` (`student_id`),
  ADD KEY `fk_question` (`question_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `answers`
--
ALTER TABLE `answers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `evaluations`
--
ALTER TABLE `evaluations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=147;

--
-- AUTO_INCREMENT for table `evaluators`
--
ALTER TABLE `evaluators`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `question`
--
ALTER TABLE `question`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `question_paper`
--
ALTER TABLE `question_paper`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT for table `question_paper_question`
--
ALTER TABLE `question_paper_question`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `student_answer`
--
ALTER TABLE `student_answer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `answers`
--
ALTER TABLE `answers`
  ADD CONSTRAINT `answers_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`);

--
-- Constraints for table `evaluations`
--
ALTER TABLE `evaluations`
  ADD CONSTRAINT `evaluations_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `evaluations_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`);

--
-- Constraints for table `question`
--
ALTER TABLE `question`
  ADD CONSTRAINT `question_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `evaluators` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `fk_evaluator` FOREIGN KEY (`created_by`) REFERENCES `evaluators` (`id`);

--
-- Constraints for table `question_paper`
--
ALTER TABLE `question_paper`
  ADD CONSTRAINT `question_paper_ibfk_1` FOREIGN KEY (`evaluator_id`) REFERENCES `evaluators` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `question_paper_question`
--
ALTER TABLE `question_paper_question`
  ADD CONSTRAINT `question_paper_question_ibfk_1` FOREIGN KEY (`question_paper_id`) REFERENCES `question_paper` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `question_paper_question_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `student_answer`
--
ALTER TABLE `student_answer`
  ADD CONSTRAINT `fk_question` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`),
  ADD CONSTRAINT `fk_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
