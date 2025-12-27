<?php
// Configuração do banco MySQL
define('DB_HOST', 'localhost');
define('DB_USER', 'gam_user');          // Novo usuário
define('DB_PASS', 'faculdade123');      // Senha que você definiu
define('DB_NAME', 'gampy');             // ⬅️ Nome CORRETO do banco!

function getConnection() {
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    if ($conn->connect_error) {
        die("Erro de conexão: " . $conn->connect_error);
    }
    
    $conn->set_charset("utf8");
    return $conn;
}
?>
