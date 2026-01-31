<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");

require_once '../config/database.php';

$data = json_decode(file_get_contents("php://input"));

if (!empty($data->nome) && !empty($data->email) && !empty($data->senha)) {
    
    // Verificar se email já existe
    $check_email = "SELECT id FROM usuario WHERE email = ?";
    $stmt = $conn->prepare($check_email);
    $stmt->bind_param("s", $data->email);
    $stmt->execute();
    $stmt->store_result();
    
    if ($stmt->num_rows > 0) {
        echo json_encode([
            "success" => false,
            "message" => "Este email já está cadastrado"
        ]);
        exit;
    }
    
    // Hash da senha (IMPORTANTE!)
    $senha_hash = password_hash($data->senha, PASSWORD_DEFAULT);
    
    // Preparar query
    $query = "INSERT INTO usuario (
        nome, 
        sobrenome, 
        email, 
        cpf, 
        senha, 
        tipo,
        telefone,
        data_nascimento,
        curso_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
    
    $stmt = $conn->prepare($query);
    
    // Definir curso_id como NULL se não for estudante
    $curso_id = ($data->tipo === 'estudante' && !empty($data->curso_id)) ? $data->curso_id : NULL;
    
    $stmt->bind_param(
        "ssssssssi",
        $data->nome,
        $data->sobrenome,
        $data->email,
        $data->cpf,
        $senha_hash,
        $data->tipo,
        $data->telefone,
        $data->data_nascimento,
        $curso_id
    );
    
    if ($stmt->execute()) {
        echo json_encode([
            "success" => true,
            "message" => "Usuário cadastrado com sucesso!"
        ]);
    } else {
        echo json_encode([
            "success" => false,
            "message" => "Erro ao cadastrar usuário: " . $conn->error
        ]);
    }
    
} else {
    echo json_encode([
        "success" => false,
        "message" => "Dados incompletos"
    ]);
}

$conn->close();
?>