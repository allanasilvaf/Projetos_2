<?php
function getConnection() {
    $host = 'localhost';
    $db = 'gampy';
    $user = 'gam_user';    // ← CORRETO
    $pass = 'gampy0';      // ← CORRETO
    
    $conn = new mysqli($host, $user, $pass, $db);
    
    if ($conn->connect_error) {
        http_response_code(500);
        die(json_encode([
            "success" => false,
            "message" => "Erro de conexão com o banco de dados"
        ]));
    }
    
    $conn->set_charset("utf8mb4");
    return $conn;
}
?>
