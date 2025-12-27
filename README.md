# 🚀 Instalação Rápida - GAM.py

## 📋 Pré-requisitos
Antes de começar, instale:
- [Node.js](https://nodejs.org/) (versão 16+)
- [PHP](https://www.php.net/) (versão 7.4+)
- [MySQL](https://www.mysql.com/) ou MariaDB

## 🛠️ Passo a Passo

### 1. Clone o repositório
```bash
git clone https://github.com/allanasilvaf/Projetos_2.git
cd Projetos_2

###2. Configure o banco de dados
mysql -u root -p <<EOF
CREATE DATABASE gam_db;
USE gam_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'professor', 'estudante') DEFAULT 'estudante',
    sobrenome VARCHAR(100),
    cpf VARCHAR(14) UNIQUE,
    telefone VARCHAR(20),
    data_nascimento DATE,
    endereco TEXT,
    curso_id INT,
    semestre INT,
    matricula VARCHAR(20) UNIQUE,
    foto VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuários de teste
INSERT INTO usuarios (nome, email, senha, tipo) VALUES 
('Administrador', 'admin@faculdade.edu', SHA2('admin123', 256), 'admin'),
('Professor Teste', 'professor@faculdade.edu', SHA2('prof123', 256), 'professor'),
('Aluno Teste', 'aluno@faculdade.edu', SHA2('aluno123', 256), 'estudante');
EOF
 
###3. Configure o backend PHP
cd backend
# Edite o arquivo config/database.php com suas credenciais do MySQL
cp config/database.example.php config/database.php
nano config/database.php

# Inicie o servidor PHP (mantenha este terminal aberto)
php -S localhost:8000
 
###4. Configure o frontend Vue.js
# Em um NOVO terminal, volte para a pasta do projeto
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run serve
 
###5. Acesse o sistema
    🌐 URL do frontend: http://localhost:8080

    🔧 URL da API: http://localhost:8000/api/

    🔐 Credenciais para teste:

        Admin: admin@faculdade.edu / admin123

        Professor: professor@faculdade.edu / prof123

        Aluno: aluno@faculdade.edu / aluno123
