<?php
/**
 * API de Telemetria - BackupMaster
 * Endpoint para obter estatísticas públicas e admin
 */

require_once 'config.php';

setCORSHeaders();

$pdo = getDB();
$method = $_SERVER['REQUEST_METHOD'];

// GET - Obter estatísticas
if ($method === 'GET') {
    $type = $_GET['type'] ?? 'public';
    
    if ($type === 'public') {
        // Estatísticas públicas
        $stmt = $pdo->query("SELECT * FROM global_stats");
        $stats = $stmt->fetch();
        
        // Calcula terabytes
        $stats['total_tb'] = round($stats['total_bytes_original'] / (1024 ** 4), 2);
        $stats['total_tb_compressed'] = round($stats['total_bytes_compressed'] / (1024 ** 4), 2);
        
        jsonResponse([
            'success' => true,
            'data' => $stats
        ]);
        
    } elseif ($type === 'admin') {
        // Requer autenticação
        $password = $_GET['password'] ?? '';
        
        if (!validateAdminPassword($password)) {
            jsonResponse([
                'success' => false,
                'error' => 'Invalid admin password'
            ], 401);
        }
        
        // Busca usuários com estatísticas
        $stmt = $pdo->query("
            SELECT 
                u.name,
                u.email,
                u.token,
                u.organization,
                u.last_validation,
                s.total_backups,
                s.total_bytes_original,
                s.last_backup
            FROM users u
            LEFT JOIN user_stats s ON u.token = s.user_token
            ORDER BY s.total_backups DESC
        ");
        
        $users = $stmt->fetchAll();
        
        // Formata dados
        foreach ($users as &$user) {
            $user['tb'] = round($user['total_bytes_original'] / (1024 ** 4), 2);
            unset($user['total_bytes_original']);
        }
        
        jsonResponse([
            'success' => true,
            'data' => $users
        ]);
    }
}

// POST - Registrar/Atualizar usuário
elseif ($method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input) {
        jsonResponse(['success' => false, 'error' => 'Invalid JSON'], 400);
    }
    
    $action = $input['action'] ?? '';
    
    if ($action === 'register') {
        // Registrar novo usuário
        $stmt = $pdo->prepare("
            INSERT INTO users (token, name, email, organization, machine_id, registered_at, last_validation, version)
            VALUES (:token, :name, :email, :organization, :machine_id, :registered_at, :last_validation, :version)
            ON DUPLICATE KEY UPDATE
                last_validation = :last_validation,
                version = :version
        ");
        
        $stmt->execute([
            'token' => $input['token'],
            'name' => $input['name'],
            'email' => $input['email'],
            'organization' => $input['organization'] ?? null,
            'machine_id' => $input['machine_id'],
            'registered_at' => $input['registered_at'],
            'last_validation' => $input['last_validation'],
            'version' => $input['version'] ?? '1.0.0'
        ]);
        
        // Log evento
        $stmt = $pdo->prepare("
            INSERT INTO events (event_type, user_token, data, ip_address)
            VALUES ('registration', :token, :data, :ip)
        ");
        
        $stmt->execute([
            'token' => $input['token'],
            'data' => json_encode($input),
            'ip' => getClientIP()
        ]);
        
        jsonResponse(['success' => true, 'message' => 'User registered']);
        
    } elseif ($action === 'update_stats') {
        // Atualizar estatísticas do usuário
        $stmt = $pdo->prepare("
            INSERT INTO user_stats (
                user_token, total_backups, total_bytes_original, total_bytes_compressed,
                total_files, format_zip, format_7z, format_targz, format_tarbz2,
                incremental_backups, full_backups, first_backup, last_backup
            ) VALUES (
                :token, :total_backups, :total_bytes_original, :total_bytes_compressed,
                :total_files, :format_zip, :format_7z, :format_targz, :format_tarbz2,
                :incremental_backups, :full_backups, :first_backup, :last_backup
            )
            ON DUPLICATE KEY UPDATE
                total_backups = :total_backups,
                total_bytes_original = :total_bytes_original,
                total_bytes_compressed = :total_bytes_compressed,
                total_files = :total_files,
                format_zip = :format_zip,
                format_7z = :format_7z,
                format_targz = :format_targz,
                format_tarbz2 = :format_tarbz2,
                incremental_backups = :incremental_backups,
                full_backups = :full_backups,
                last_backup = :last_backup
        ");
        
        $formats = $input['backups_by_format'] ?? [];
        
        $stmt->execute([
            'token' => $input['token'],
            'total_backups' => $input['total_backups'] ?? 0,
            'total_bytes_original' => $input['total_bytes_original'] ?? 0,
            'total_bytes_compressed' => $input['total_bytes_compressed'] ?? 0,
            'total_files' => $input['total_files'] ?? 0,
            'format_zip' => $formats['zip'] ?? 0,
            'format_7z' => $formats['7z'] ?? 0,
            'format_targz' => $formats['tar.gz'] ?? 0,
            'format_tarbz2' => $formats['tar.bz2'] ?? 0,
            'incremental_backups' => $input['incremental_backups'] ?? 0,
            'full_backups' => $input['full_backups'] ?? 0,
            'first_backup' => $input['first_backup'] ?? null,
            'last_backup' => $input['last_backup'] ?? null
        ]);
        
        jsonResponse(['success' => true, 'message' => 'Stats updated']);
        
    } elseif ($action === 'download') {
        // Registrar download
        $stmt = $pdo->prepare("
            INSERT INTO downloads (platform, version, ip_address, user_agent)
            VALUES (:platform, :version, :ip, :user_agent)
        ");
        
        $stmt->execute([
            'platform' => $input['platform'],
            'version' => $input['version'] ?? '1.0.0',
            'ip' => getClientIP(),
            'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? null
        ]);
        
        jsonResponse(['success' => true, 'message' => 'Download recorded']);
    }
}

else {
    jsonResponse(['success' => false, 'error' => 'Method not allowed'], 405);
}
