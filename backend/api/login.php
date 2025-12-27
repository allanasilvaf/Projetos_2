<?php
header("Access-Control-Allow-Origin: http://localhost:8080");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");

require_once '../config/database.php';

// Ler dados JSON do Vue.js
$data = json_decode(file_get_contents("php://input"));

if (!empty($data->email) && !empty($data->senha)) {
    $conn = getConnection();
    
    // Buscar usuário pelo email
    $stmt = $conn->prepare("SELECT id, nome, email, senha, tipo FROM usuarios WHERE email = ?");
    $stmt->bind_param("s", $data->email);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        
        // Verificar senha (hash)
        if (password_verify($data->senha, $user['senha'])) {
            // Login bem-sucedido
            unset($user['senha']); // Remover senha da resposta
            
            echo json_encode([
                "success" => true,
                "message" => "Login realizado com sucesso!",
                "user" => $user
            ]);
        } else {
            echo json_encode([
                "success" => false,
                "message" => "Senha incorreta!"
            ]);
        }
    } else {
        echo json_encode([
            "success" => false, 
            "message" => "Usuário não encontrado!"
        ]);
    }
    
    $stmt->close();
    $conn->close();
} else {
    echo json_encode([
        "success" => false,
        "message" => "Email e senha são obrigatórios!"
    ]);
}
?>
