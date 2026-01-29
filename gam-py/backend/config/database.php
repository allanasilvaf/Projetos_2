<?php
// Configuração do banco MySQL - Ajustado para o seu ambiente local
define('DB_HOST', 'localhost');
define('DB_USER', 'root');           // Usuário padrão do seu MySQL
define('DB_PASS', 'ricklindo1503');  // A senha do seu banco
define('DB_NAME', 'gam_db');         // O nome do banco que criamos no SQL

// Adicionando cabeçalhos para evitar erro de CORS no futuro
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");

function getConnection() {
    // Usando @ para suprimir warnings na tela e evitar erro no JSON
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    if ($conn->connect_error) {
        // Retorna erro em JSON para o Frontend entender, em vez de texto puro
        die(json_encode(["error" => "Falha na conexão: " . $conn->connect_error]));
    }
    
    $conn->set_charset("utf8");
    return $conn;
}
?>