// Dashboard de Telemetria - BackupMaster
// Dados simulados (em produção, viriam de uma API)

const ADMIN_PASSWORD = 'backupmaster2025'; // Altere para uma senha segura

// Dados de exemplo
let telemetryData = {
    totalUsers: 1250,
    activeUsers: 890,
    totalBackups: 187500,
    totalTB: 6250.50,
    downloads: {
        windows: 750,
        linux: 320,
        macos: 180
    },
    formats: {
        zip: 45000,
        '7z': 98000,
        targz: 32500,
        tarbz2: 12000
    },
    users: [
        {
            name: 'João Silva',
            email: 'joao@email.com',
            token: 'a1b2c3d4e5f6g7h8',
            backups: 150,
            tb: 5.2,
            lastAccess: '2025-12-05'
        },
        {
            name: 'Maria Santos',
            email: 'maria@empresa.com',
            token: 'x9y8z7w6v5u4t3s2',
            backups: 89,
            tb: 3.8,
            lastAccess: '2025-12-04'
        },
        {
            name: 'Pedro Costa',
            email: 'pedro@tech.com',
            token: 'p1q2r3s4t5u6v7w8',
            backups: 234,
            tb: 12.5,
            lastAccess: '2025-12-05'
        },
        {
            name: 'Ana Oliveira',
            email: 'ana@startup.io',
            token: 'm9n8o7p6q5r4s3t2',
            backups: 67,
            tb: 2.1,
            lastAccess: '2025-12-03'
        },
        {
            name: 'Carlos Mendes',
            email: 'carlos@dev.com',
            token: 'c1d2e3f4g5h6i7j8',
            backups: 412,
            tb: 18.9,
            lastAccess: '2025-12-05'
        }
    ]
};

// Estado da aplicação
let isAdminLoggedIn = false;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    setupEventListeners();
});

// Carrega dados do dashboard
function loadDashboardData() {
    // Atualiza estatísticas principais
    animateNumber('totalUsers', telemetryData.totalUsers);
    animateNumber('activeUsers', telemetryData.activeUsers);
    animateNumber('totalBackups', telemetryData.totalBackups);
    animateNumber('totalTB', telemetryData.totalTB, true);

    // Atualiza gráfico de downloads
    updateDownloadsChart();

    // Atualiza gráfico de formatos
    updateFormatsChart();
}

// Anima números
function animateNumber(elementId, targetValue, isDecimal = false) {
    const element = document.getElementById(elementId);
    const duration = 2000;
    const steps = 60;
    const increment = targetValue / steps;
    let current = 0;

    const timer = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(timer);
        }
        
        if (isDecimal) {
            element.textContent = current.toFixed(2) + ' TB';
        } else {
            element.textContent = Math.floor(current).toLocaleString('pt-BR');
        }
    }, duration / steps);
}

// Atualiza gráfico de downloads
function updateDownloadsChart() {
    const total = telemetryData.downloads.windows + 
                  telemetryData.downloads.linux + 
                  telemetryData.downloads.macos;

    updateBar('downloadsWindows', 'downloadsWindowsBar', 
              telemetryData.downloads.windows, total);
    updateBar('downloadsLinux', 'downloadsLinuxBar', 
              telemetryData.downloads.linux, total);
    updateBar('downloadsMacOS', 'downloadsMacOSBar', 
              telemetryData.downloads.macos, total);
}

// Atualiza gráfico de formatos
function updateFormatsChart() {
    const total = telemetryData.formats.zip + 
                  telemetryData.formats['7z'] + 
                  telemetryData.formats.targz + 
                  telemetryData.formats.tarbz2;

    updateBar('formatZip', 'formatZipBar', 
              telemetryData.formats.zip, total);
    updateBar('format7z', 'format7zBar', 
              telemetryData.formats['7z'], total);
    updateBar('formatTarGz', 'formatTarGzBar', 
              telemetryData.formats.targz, total);
}

// Atualiza barra de progresso
function updateBar(textId, barId, value, total) {
    const percentage = (value / total) * 100;
    
    document.getElementById(textId).textContent = value.toLocaleString('pt-BR');
    
    setTimeout(() => {
        document.getElementById(barId).style.width = percentage + '%';
    }, 100);
}

// Configura event listeners
function setupEventListeners() {
    // Botão Admin
    document.getElementById('adminBtn').addEventListener('click', showLoginModal);

    // Botão Logout
    document.getElementById('logoutBtn').addEventListener('click', logout);

    // Botão Cancelar
    document.getElementById('cancelBtn').addEventListener('click', hideLoginModal);

    // Form de login
    document.getElementById('loginForm').addEventListener('submit', handleLogin);

    // Busca
    document.getElementById('searchInput').addEventListener('input', filterUsers);
}

// Mostra modal de login
function showLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
    document.getElementById('loginModal').classList.add('flex');
    document.getElementById('adminPassword').focus();
}

// Esconde modal de login
function hideLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('loginModal').classList.remove('flex');
    document.getElementById('adminPassword').value = '';
}

// Handle login
function handleLogin(e) {
    e.preventDefault();
    
    const password = document.getElementById('adminPassword').value;
    
    if (password === ADMIN_PASSWORD) {
        isAdminLoggedIn = true;
        hideLoginModal();
        showAdminSection();
        loadUsersTable();
    } else {
        alert('Senha incorreta!');
        document.getElementById('adminPassword').value = '';
        document.getElementById('adminPassword').focus();
    }
}

// Logout
function logout() {
    isAdminLoggedIn = false;
    hideAdminSection();
}

// Mostra seção admin
function showAdminSection() {
    document.getElementById('adminSection').classList.add('active');
    document.getElementById('adminBtn').innerHTML = '<i class="fas fa-user-shield mr-2"></i>Admin (Logado)';
    document.getElementById('adminBtn').classList.add('bg-green-500', 'text-white');
    document.getElementById('adminBtn').classList.remove('bg-white', 'text-purple-600');
}

// Esconde seção admin
function hideAdminSection() {
    document.getElementById('adminSection').classList.remove('active');
    document.getElementById('adminBtn').innerHTML = '<i class="fas fa-lock mr-2"></i>Admin';
    document.getElementById('adminBtn').classList.remove('bg-green-500', 'text-white');
    document.getElementById('adminBtn').classList.add('bg-white', 'text-purple-600');
}

// Carrega tabela de usuários
function loadUsersTable(users = telemetryData.users) {
    const tbody = document.getElementById('usersTable');
    tbody.innerHTML = '';

    users.forEach(user => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50 transition';
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                        <span class="text-purple-600 font-bold">${user.name.charAt(0)}</span>
                    </div>
                    <div class="text-sm font-medium text-gray-900">${user.name}</div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${user.email}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <code class="text-xs bg-gray-100 px-3 py-1 rounded font-mono">${user.token}</code>
                    <button onclick="copyToken('${user.token}')" class="ml-2 text-gray-400 hover:text-gray-600">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${user.backups.toLocaleString('pt-BR')}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-semibold text-orange-600">${user.tb.toFixed(2)} TB</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">${formatDate(user.lastAccess)}</div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Filtra usuários
function filterUsers(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    const filtered = telemetryData.users.filter(user => 
        user.name.toLowerCase().includes(searchTerm) ||
        user.email.toLowerCase().includes(searchTerm) ||
        user.token.toLowerCase().includes(searchTerm)
    );
    
    loadUsersTable(filtered);
}

// Copia token
function copyToken(token) {
    navigator.clipboard.writeText(token).then(() => {
        // Mostra feedback visual
        const btn = event.target.closest('button');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check text-green-600"></i>';
        
        setTimeout(() => {
            btn.innerHTML = originalHTML;
        }, 2000);
    });
}

// Formata data
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Hoje';
    if (diffDays === 1) return 'Ontem';
    if (diffDays < 7) return `${diffDays} dias atrás`;
    
    return date.toLocaleDateString('pt-BR');
}

// Simula atualização em tempo real
setInterval(() => {
    // Incrementa valores aleatoriamente
    if (Math.random() > 0.7) {
        telemetryData.totalBackups += Math.floor(Math.random() * 10);
        telemetryData.totalTB += Math.random() * 0.5;
        
        document.getElementById('totalBackups').textContent = 
            telemetryData.totalBackups.toLocaleString('pt-BR');
        document.getElementById('totalTB').textContent = 
            telemetryData.totalTB.toFixed(2) + ' TB';
    }
}, 5000);
