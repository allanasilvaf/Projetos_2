<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

// Tratamento para requisições de pré-voo (CORS)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Conexão com o banco (Use as credenciais do seu docker-compose)
$host = getenv('DB_HOST') ?: 'mysql';
$dbname = getenv('DB_NAME') ?: 'gampy';
$user = getenv('DB_USER') ?: 'gam_user';
$pass = getenv('DB_PASSWORD') ?: 'gampy0';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo json_encode(["success" => false, "message" => "Erro de conexão: " . $e->getMessage()]);
    exit;
}

// Lógica para o método PUT (Atualização)
if ($_SERVER['REQUEST_METHOD'] === 'PUT') {
    
    $path = explode('/', $_SERVER['REQUEST_URI']);
    $id = end($path);

    // Lê o corpo da requisição (JSON)
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    if (isset($data['semestre']) && $id) {
        try {
            // Atualiza a tabela (agora com a coluna semestre que você criou)
            $stmt = $pdo->prepare("UPDATE usuario SET semestre = ? WHERE id = ?");
            $stmt->execute([$data['semestre'], $id]);

            echo json_encode([
                "success" => true, 
                "message" => " Dados atualizados com sucesso!",
                "semestre" => $data['semestre']
            ]);
        } catch (Exception $e) {
            http_response_code(500);
            echo json_encode(["success" => false, "message" => "Erro ao atualizar: " . $e->getMessage()]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["success" => false, "message" => "Dados incompletos."]);
    }
}
?>