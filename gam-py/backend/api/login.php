<?php
// Headers CORS CORRETOS para Vue.js na porta 5173
header("Access-Control-Allow-Origin: http://localhost:5173");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Accept, Authorization, X-Requested-With");
header("Access-Control-Allow-Credentials: true");
header("Access-Control-Max-Age: 3600");

// Permitir requisições OPTIONS (pré-flight do CORS)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

require_once '../config/database.php';

// Ler dados JSON do Vue.js
$data = json_decode(file_get_contents("php://input"));

// VALIDAÇÃO melhorada
if (empty($data) || !isset($data->email) || !isset($data->senha)) {
    http_response_code(400);
    echo json_encode([
        "success" => false,
        "message" => "Email e senha são obrigatórios!"
    ]);
    exit();
}

// Remover espaços
$email = trim($data->email);
$senha = trim($data->senha);

if (empty($email) || empty($senha)) {
    http_response_code(400);
    echo json_encode([
        "success" => false,
        "message" => "Email e senha não podem estar vazios!"
    ]);
    exit();
}

try {
    $conn = getConnection();
    
    // Buscar usuário pelo email
    $stmt = $conn->prepare("SELECT id, nome, email, senha, tipo FROM usuario WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows === 0) {
        http_response_code(404);
        echo json_encode([
            "success" => false,
            "message" => "Usuário não encontrado!"
        ]);
        exit();
    }
    
    $user = $result->fetch_assoc();
    
    // Verificar senha (hash)
    if (!password_verify($senha, $user['senha'])) {
        http_response_code(401);
        echo json_encode([
            "success" => false,
            "message" => "Senha incorreta!"
        ]);
        exit();
    }
    
    // Login bem-sucedido
    unset($user['senha']); // Remover senha da resposta
    
    // Estrutura que seu Vue.js espera
    echo json_encode([
        "success" => true,
        "message" => "Login realizado com sucesso!",
        "user" => $user  // ← "user" (inglês)
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        "success" => false,
        "message" => "Erro no servidor: " . $e->getMessage()
    ]);
} finally {
    if (isset($stmt)) $stmt->close();
    if (isset($conn)) $conn->close();
}
?>
