<?php
/**
 * Configuração do Banco de Dados
 * 
 * INSTRUÇÕES:
 * 1. Renomeie este arquivo para config.php
 * 2. Preencha com as credenciais do MySQL da Hostinger
 * 3. NÃO commite este arquivo no Git (está no .gitignore)
 */

// Configurações do MySQL (Hostinger)
define('DB_HOST', 'localhost'); // ou o host fornecido pela Hostinger
define('DB_NAME', 'backupmaster_telemetry');
define('DB_USER', 'seu_usuario_mysql');
define('DB_PASS', 'sua_senha_mysql');
define('DB_CHARSET', 'utf8mb4');

// Senha do Admin (para acessar dados sensíveis)
define('ADMIN_PASSWORD', 'backupmaster2025'); // ALTERE ESTA SENHA!

// Configurações de CORS
define('ALLOWED_ORIGINS', [
    'http://localhost:8000',
    'https://seu-dominio.com',
    'https://eduradopessoa.github.io'
]);

// Timezone
date_default_timezone_set('America/Sao_Paulo');

// Configurações de erro (desabilite em produção)
ini_set('display_errors', 0);
error_reporting(E_ALL);

// Função para conectar ao banco
function getDB() {
    static $pdo = null;
    
    if ($pdo === null) {
        try {
            $dsn = sprintf(
                'mysql:host=%s;dbname=%s;charset=%s',
                DB_HOST,
                DB_NAME,
                DB_CHARSET
            );
            
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ];
            
            $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        } catch (PDOException $e) {
            http_response_code(500);
            die(json_encode([
                'error' => 'Database connection failed',
                'message' => $e->getMessage()
            ]));
        }
    }
    
    return $pdo;
}

// Função para configurar CORS
function setCORSHeaders() {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    
    if (in_array($origin, ALLOWED_ORIGINS)) {
        header("Access-Control-Allow-Origin: $origin");
    }
    
    header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization');
    header('Access-Control-Max-Age: 86400');
    
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit;
    }
}

// Função para validar senha de admin
function validateAdminPassword($password) {
    return hash_equals(ADMIN_PASSWORD, $password);
}

// Função para obter IP do cliente
function getClientIP() {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ip = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0];
    }
    
    return $ip;
}

// Função para responder JSON
function jsonResponse($data, $status = 200) {
    http_response_code($status);
    header('Content-Type: application/json');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}
