<?php
require_once 'config/database.php';

echo "🔍 Testando conexão MySQL...\n";

try {
    $conn = getConnection();
    echo "✅ Conexão estabelecida!\n\n";
    
    // Testar consulta
    echo "📊 Testando consulta à tabela 'usuarios'...\n";
    $result = $conn->query("SELECT COUNT(*) as total FROM usuarios");
    $row = $result->fetch_assoc();
    echo "   Total de usuários: " . $row['total'] . "\n\n";
    
    // Listar usuários
    echo "👥 Listando usuários:\n";
    $result = $conn->query("SELECT id, nome, email, tipo, LEFT(senha, 30) as hash FROM usuarios");
    while ($row = $result->fetch_assoc()) {
        echo "   - ID: " . $row['id'] . " | " . $row['email'] . " (" . $row['tipo'] . ")\n";
        echo "     Hash: " . $row['hash'] . "...\n";
    }
    
    // Testar password_verify
    echo "\n🔐 Testando password_verify...\n";
    $email = "professor@faculdade.edu";
    $senha = "123456";
    
    $stmt = $conn->prepare("SELECT senha FROM usuarios WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        if (password_verify($senha, $user['senha'])) {
            echo "   ✅ password_verify('123456', hash): CORRETO!\n";
        } else {
            echo "   ❌ password_verify('123456', hash): FALHOU!\n";
            echo "   Tente gerar novo hash: php -r \"echo password_hash('123456', PASSWORD_DEFAULT);\"\n";
        }
    }
    
    $conn->close();
    echo "\n🎉 Todos os testes concluídos!\n";
    
} catch (Exception $e) {
    echo "❌ Erro: " . $e->getMessage() . "\n";
    echo "Dica: Verifique se o usuário 'gam_user' tem acesso ao banco 'gampy'\n";
}
?>
