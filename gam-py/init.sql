CREATE DATABASE IF NOT EXISTS gampy;
USE gampy;

CREATE TABLE usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    sobrenome VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'professor', 'estudante') NOT NULL DEFAULT 'estudante',
    telefone VARCHAR(20),
    data_nascimento DATE,
    curso_id INT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    semestre VARCHAR(20) DEFAULT NULL
);

INSERT INTO usuario (nome, email, cpf, senha, tipo) VALUES
('Administrador', 'admin@faculdade.edu', '11122233344', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin'),
('Professor Teste', 'professor@faculdade.edu', '22233344455', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'professor'),
('Aluno Teste', 'aluno@faculdade.edu', '33344455566', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'estudante');
