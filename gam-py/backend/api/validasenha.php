<?php
// Cabeçalhos CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit;
}

// Importa o seu arquivo de conexão (ajuste o caminho se necessário)
require_once '../config/database.php'; 

$conn = getConnection();
$data = json_decode(file_get_contents("php://input"), true);

if (!empty($data['email']) && !empty($data['cpf'])) {
    $email = $data['email'];
    $cpf = $data['cpf'];

    // Usando Prepared Statements com MySQLi (mais seguro contra SQL Injection)
    $stmt = $conn->prepare("SELECT id FROM usuario WHERE email = ? AND cpf = ? LIMIT 1");
    $stmt->bind_param("ss", $email, $cpf);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["success" => false, "message" => "E-mail ou CPF não encontrados."]);
    }

    $stmt->close();
} else {
    echo json_encode(["success" => false, "message" => "Dados incompletos."]);
}

$conn->close();