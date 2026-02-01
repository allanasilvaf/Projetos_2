<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit;
}

// Usando o caminho que você confirmou que funciona!
require_once __DIR__ . '/../config/database.php'; 

$conn = getConnection();
$data = json_decode(file_get_contents("php://input"), true);

if (!empty($data['email']) && !empty($data['novaSenha'])) {
    $email = $data['email'];
    
    // CRIPTOGRAFIA: O professor vai cobrar isso! 
    // Nunca salve senha em texto puro no banco.
    $senhaHash = password_hash($data['novaSenha'], PASSWORD_DEFAULT);

    $stmt = $conn->prepare("UPDATE usuario SET senha = ? WHERE email = ?");
    $stmt->bind_param("ss", $senhaHash, $email);

    if ($stmt->execute()) {
        echo json_encode(["success" => true]);
    } else {
        echo json_encode(["success" => false, "message" => "Erro ao atualizar no banco."]);
    }
    $stmt->close();
} else {
    echo json_encode(["success" => false, "message" => "Dados insuficientes."]);
}

$conn->close();