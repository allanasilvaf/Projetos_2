-- database/create_tables.sql
-- Estrutura EXATA da tabela usuario do sistema GAM.py

CREATE DATABASE IF NOT EXISTS gampy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gampy;

-- Tabela usuario (ESTRUTURA REAL DO SEU SISTEMA)
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
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SELECT '✅ Estrutura do banco criada com sucesso!' as mensagem;
