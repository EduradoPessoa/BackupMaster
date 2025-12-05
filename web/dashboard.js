// Dashboard de Telemetria - BackupMaster
// Conectado ao MySQL via API PHP

const ADMIN_PASSWORD = 'backupmaster2025'; // Altere para uma senha segura

// URL da API (altere para seu domínio da Hostinger)
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api/telemetry.php'
    : 'https://seu-dominio.com/api/telemetry.php';

// Dados carregados da API
let telemetryData = {
    totalUsers: 0,
    activeUsers: 0,
    totalBackups: 0,
    totalTB: 0,
    downloads: {
        windows: 0,
        linux: 0,
        macos: 0
    },
    formats: {
        zip: 0,
        '7z': 0,
        targz: 0,
        tarbz2: 0
    },
    users: []
};

// Estado da aplicação
let isAdminLoggedIn = false;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    loadPublicData();
    setupEventListeners();
});

// Carrega dados públicos da API
async function loadPublicData() {
    try {
        const response = await fetch(`${API_URL}?type=public`);
        const result = await response.json();

        if (result.success) {
            const data = result.data;

            // Atualiza telemetryData
            telemetryData.totalUsers = parseInt(data.total_users) || 0;
            telemetryData.activeUsers = parseInt(data.active_users_30d) || 0;
            telemetryData.totalBackups = parseInt(data.total_backups) || 0;
            telemetryData.totalTB = parseFloat(data.total_tb) || 0;

            telemetryData.downloads = {
                windows: parseInt(data.downloads_windows) || 0,
                linux: parseInt(data.downloads_linux) || 0,
                macos: parseInt(data.downloads_macos) || 0
            };

            telemetryData.formats = {
                zip: parseInt(data.format_zip) || 0,
                '7z': parseInt(data.format_7z) || 0,
                targz: parseInt(data.format_targz) || 0,
                tarbz2: parseInt(data.format_tarbz2) || 0
            };

            loadDashboardData();
        }
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        // Usa dados de fallback
        loadDashboardData();
    }
}

// Carrega dados de admin da API
async function loadAdminData(password) {
    try {
        const response = await fetch(`${API_URL}?type=admin&password=${encodeURIComponent(password)}`);
        const result = await response.json();

        if (result.success) {
            telemetryData.users = result.data.map(user => ({
                name: user.name,
                email: user.email,
                token: user.token,
                backups: parseInt(user.total_backups) || 0,
                tb: parseFloat(user.tb) || 0,
                lastAccess: user.last_validation || user.last_backup
            }));

            loadUsersTable();
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error('Erro ao carregar dados admin:', error);
        return false;
    }
}

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
async function handleLogin(e) {
    e.preventDefault();

    const password = document.getElementById('adminPassword').value;

    // Tenta carregar dados admin
    const success = await loadAdminData(password);

    if (success) {
        isAdminLoggedIn = true;
        hideLoginModal();
        showAdminSection();
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

// Atualiza dados periodicamente
setInterval(() => {
    loadPublicData();
}, 30000); // A cada 30 segundos
