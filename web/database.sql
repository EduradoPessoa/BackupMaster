-- Banco de Dados para BackupMaster Telemetry
-- Execute este script no MySQL da Hostinger

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS backupmaster_telemetry 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE backupmaster_telemetry;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    organization VARCHAR(255) DEFAULT NULL,
    machine_id VARCHAR(32) NOT NULL,
    registered_at DATETIME NOT NULL,
    last_validation DATETIME NOT NULL,
    version VARCHAR(20) DEFAULT '1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_token (token),
    INDEX idx_email (email),
    INDEX idx_last_validation (last_validation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de estatísticas de usuários
CREATE TABLE IF NOT EXISTS user_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_token VARCHAR(64) NOT NULL,
    total_backups INT DEFAULT 0,
    total_bytes_original BIGINT DEFAULT 0,
    total_bytes_compressed BIGINT DEFAULT 0,
    total_files INT DEFAULT 0,
    format_zip INT DEFAULT 0,
    format_7z INT DEFAULT 0,
    format_targz INT DEFAULT 0,
    format_tarbz2 INT DEFAULT 0,
    incremental_backups INT DEFAULT 0,
    full_backups INT DEFAULT 0,
    first_backup DATETIME DEFAULT NULL,
    last_backup DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_token) REFERENCES users(token) ON DELETE CASCADE,
    INDEX idx_user_token (user_token),
    INDEX idx_last_backup (last_backup)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de downloads
CREATE TABLE IF NOT EXISTS downloads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(20) NOT NULL, -- windows, linux, macos
    version VARCHAR(20) NOT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    user_agent TEXT DEFAULT NULL,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_platform (platform),
    INDEX idx_version (version),
    INDEX idx_downloaded_at (downloaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de eventos (log de atividades)
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL, -- registration, backup, download, etc
    user_token VARCHAR(64) DEFAULT NULL,
    data JSON DEFAULT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_event_type (event_type),
    INDEX idx_user_token (user_token),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- View para estatísticas globais
CREATE OR REPLACE VIEW global_stats AS
SELECT 
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT CASE 
        WHEN u.last_validation >= DATE_SUB(NOW(), INTERVAL 30 DAY) 
        THEN u.id 
    END) as active_users_30d,
    COALESCE(SUM(s.total_backups), 0) as total_backups,
    COALESCE(SUM(s.total_bytes_original), 0) as total_bytes_original,
    COALESCE(SUM(s.total_bytes_compressed), 0) as total_bytes_compressed,
    COALESCE(SUM(s.total_files), 0) as total_files,
    COALESCE(SUM(s.format_zip), 0) as format_zip,
    COALESCE(SUM(s.format_7z), 0) as format_7z,
    COALESCE(SUM(s.format_targz), 0) as format_targz,
    COALESCE(SUM(s.format_tarbz2), 0) as format_tarbz2,
    (SELECT COUNT(*) FROM downloads WHERE platform = 'windows') as downloads_windows,
    (SELECT COUNT(*) FROM downloads WHERE platform = 'linux') as downloads_linux,
    (SELECT COUNT(*) FROM downloads WHERE platform = 'macos') as downloads_macos
FROM users u
LEFT JOIN user_stats s ON u.token = s.user_token;

-- Inserir dados de exemplo (opcional - remova em produção)
INSERT INTO users (token, name, email, organization, machine_id, registered_at, last_validation) VALUES
('a1b2c3d4e5f6g7h8', 'João Silva', 'joao@email.com', 'Tech Corp', 'machine001', NOW(), NOW()),
('x9y8z7w6v5u4t3s2', 'Maria Santos', 'maria@empresa.com', 'StartupXYZ', 'machine002', NOW(), NOW()),
('p1q2r3s4t5u6v7w8', 'Pedro Costa', 'pedro@tech.com', NULL, 'machine003', NOW(), NOW());

INSERT INTO user_stats (user_token, total_backups, total_bytes_original, total_bytes_compressed, total_files, format_zip, format_7z, first_backup, last_backup) VALUES
('a1b2c3d4e5f6g7h8', 150, 5589934592000, 3353960755200, 45000, 30, 100, DATE_SUB(NOW(), INTERVAL 120 DAY), NOW()),
('x9y8z7w6v5u4t3s2', 89, 4076863283200, 2446117969920, 28000, 20, 60, DATE_SUB(NOW(), INTERVAL 90 DAY), DATE_SUB(NOW(), INTERVAL 1 DAY)),
('p1q2r3s4t5u6v7w8', 234, 13421772800000, 8053063680000, 78000, 50, 150, DATE_SUB(NOW(), INTERVAL 180 DAY), NOW());

INSERT INTO downloads (platform, version, ip_address) VALUES
('windows', '1.0.0', '192.168.1.1'),
('linux', '1.0.0', '192.168.1.2'),
('macos', '1.0.0', '192.168.1.3');
