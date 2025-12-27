<?php

if (php_sapi_name() !== 'cli') {
    die("esse script só pode ser executado via terminal (CLI)");
}

require_once 'config/database.php';

echo "Configurando o banco...\n";

$conn = getConnection();

// limpar a tabela de usuários 
echo "Limpando usuários antigos...\n";
$conn->query("SET FOREIGN_KEY_CHECKS = 0");
$conn->query("TRUNCATE TABLE usuarios");
$conn->query("SET FOREIGN_KEY_CHECKS = 1");

// senhas criptografadas pelo PHP
$usuarios = [
    [
        'nome' => 'Administrador',
        'email' => 'admin@faculdade.edu',
        'senha' => 'admin123', 
        'tipo' => 'admin',
        'matricula' => 'ADM001'
    ],
    [
        'nome' => 'Professor Teste',
        'email' => 'professor@faculdade.edu',
        'senha' => 'prof123',
        'tipo' => 'professor',
        'matricula' => 'PROF001'
    ],
    [
        'nome' => 'Aluno Teste',
        'email' => 'aluno@faculdade.edu',
        'senha' => 'aluno123',
        'tipo' => 'estudante',
        'matricula' => 'ALU001'
    ]
];

// inserir bd
$stmt = $conn->prepare("INSERT INTO usuarios (nome, email, senha, tipo, matricula) VALUES (?, ?, ?, ?, ?)");

foreach ($usuarios as $user) {
    $senhaHash = password_hash($user['senha'], PASSWORD_DEFAULT);
    
    $stmt->bind_param("sssss", 
        $user['nome'], 
        $user['email'], 
        $senhaHash, 
        $user['tipo'],
        $user['matricula']
    );
    
    if ($stmt->execute()) {
        echo "usuário criado: {$user['nome']} ({$user['tipo']})\n";
    } else {
        echo "erro ao criar {$user['nome']}: " . $stmt->error . "\n";
    }
}

echo "BD sincronizado";