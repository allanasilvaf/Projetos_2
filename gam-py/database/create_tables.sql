CREATE DATABASE IF NOT EXISTS gampy 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE gampy;

-- Tabela usuario (estrutura básica)
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `sobrenome` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `data_cadastro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cpf` varchar(14) DEFAULT NULL,
  `tipo` enum('estudante','professor','admin') DEFAULT 'estudante',
  `telefone` varchar(15) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `curso_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `cpf` (`cpf`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabelas para expansão futura
CREATE TABLE IF NOT EXISTS `curso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `duracao_semestres` int DEFAULT 10,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SELECT '✅ Tabelas criadas com sucesso!' as mensagem;
