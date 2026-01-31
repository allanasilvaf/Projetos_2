<?php
header("Access-Control-Allow-Origin: http://localhost:5174");
header("Content-Type: application/json");

echo json_encode([
    "api" => "GAM.py Backend API",
    "version" => "1.0",
    "status" => "online",
    "endpoints" => [
        "POST /api/login.php" => "Login de usuário",
        "GET /" => "Esta página de status"
    ],
    "database" => "MySQL - gam_faculdade",
    "project" => "Sistema de Gerenciamento Acadêmico"
]);
?>
