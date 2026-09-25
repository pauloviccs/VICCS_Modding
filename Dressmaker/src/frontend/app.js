document.addEventListener('DOMContentLoaded', () => {
  // Elementos do DOM
  const pathText = document.getElementById('path-text');
  const statusDot = document.getElementById('status-dot');
  const statusPill = document.getElementById('status-pill');
  const modInstalledStatus = document.getElementById('mod-installed-status');
  const btnBrowse = document.getElementById('btn-browse');
  const btnInstall = document.getElementById('btn-install');
  const installBtnText = document.getElementById('install-btn-text');
  const btnRestore = document.getElementById('btn-restore');
  const btnLaunch = document.getElementById('btn-launch');
  const progressContainer = document.getElementById('progress-container');
  const progressBar = document.getElementById('progress-bar');
  const progressPhaseText = document.getElementById('progress-phase-text');
  const progressPercentText = document.getElementById('progress-percent-text');
  const toastShelf = document.getElementById('toast-shelf');

  let currentStatus = null;

  // Sistema de Notificações Toast
  function showToast(message, type = 'info', duration = 4000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ℹ';
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    toastShelf.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(12px) scale(0.95)';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // Atualiza a Interface com base no status retornado pelo backend
  function updateUI(status) {
    currentStatus = status;
    pathText.textContent = status.game_dir || 'Não definido';

    // 1. Validação do Jogo
    if (status.is_valid) {
      statusDot.className = 'status-dot success';
      statusPill.textContent = 'Jogo Detectado';
      btnLaunch.disabled = false;
    } else {
      statusDot.className = 'status-dot danger';
      statusPill.textContent = 'Jogo Não Encontrado';
      btnLaunch.disabled = true;
    }

    // 2. Jogo em execução
    if (status.is_running) {
      installBtnText.textContent = 'Feche o Dressmaker para Instalar';
      btnInstall.disabled = true;
      statusDot.className = 'status-dot danger';
      statusPill.textContent = 'Jogo em Execução';
      return;
    }

    // 3. Status de Instalação do Mod
    if (status.is_installed) {
      modInstalledStatus.textContent = 'Tradução PT-BR Ativa';
      modInstalledStatus.className = 'state-val gold-accent';
      installBtnText.textContent = 'Reinstalar Tradução PT-BR';
      btnInstall.disabled = false;
    } else {
      modInstalledStatus.textContent = 'Pronto para Instalação';
      modInstalledStatus.className = 'state-val';
      installBtnText.textContent = 'Instalar Tradução PT-BR';
      btnInstall.disabled = !status.is_valid;
    }

    // 4. Backup para Restauração
    btnRestore.disabled = !status.has_backup;
  }

  // Busca o status atual no backend
  async function fetchStatus() {
    try {
      const res = await fetch('/api/status');
      if (!res.ok) throw new Error('Falha ao comunicar com o backend local');
      const data = await res.json();
      updateUI(data);
    } catch (err) {
      console.error(err);
      statusDot.className = 'status-dot danger';
      statusPill.textContent = 'Backend Offline';
      showToast('Não foi possível conectar ao servidor do instalador.', 'error');
    }
  }

  // Procurar pasta
  btnBrowse.addEventListener('click', async () => {
    try {
      showToast('Aguardando seleção da pasta...', 'info', 2500);
      const res = await fetch('/api/select_folder', { method: 'POST' });
      const data = await res.json();
      updateUI(data);
    } catch (err) {
      showToast('Erro ao selecionar pasta.', 'error');
    }
  });

  // Ação de Instalação com animação de progresso suave
  btnInstall.addEventListener('click', async () => {
    if (!currentStatus || !currentStatus.is_valid) {
      showToast('Localização do jogo inválida.', 'error');
      return;
    }

    btnInstall.disabled = true;
    btnRestore.disabled = true;
    btnLaunch.disabled = true;
    progressContainer.classList.remove('hidden');

    let currentProgress = 0;
    const updateProgress = (pct, phase) => {
      currentProgress = pct;
      progressBar.style.width = `${pct}%`;
      progressPercentText.textContent = `${pct}%`;
      progressPhaseText.textContent = phase;
    };

    updateProgress(15, 'Criando backup seguro dos arquivos originais...');

    const timer = setInterval(() => {
      if (currentProgress < 70) {
        updateProgress(currentProgress + 8, 'Costurando tabelas de textos em Português...');
      }
    }, 280);

    try {
      const res = await fetch('/api/install', { method: 'POST' });
      clearInterval(timer);
      const result = await res.json();

      if (result.success) {
        updateProgress(100, 'Tradução aplicada com perfeição!');
        showToast('Tradução PT-BR instalada com sucesso!', 'success');
        setTimeout(() => {
          progressContainer.classList.add('hidden');
          fetchStatus();
        }, 1200);
      } else {
        throw new Error(result.error || 'Erro desconhecido durante o patch.');
      }
    } catch (err) {
      clearInterval(timer);
      progressContainer.classList.add('hidden');
      showToast(err.message, 'error', 6000);
      fetchStatus();
    }
  });

  // Restaurar arquivos originais
  btnRestore.addEventListener('click', async () => {
    if (!confirm('Deseja realmente restaurar os arquivos originais do jogo e remover a tradução?')) {
      return;
    }

    btnRestore.disabled = true;
    try {
      const res = await fetch('/api/restore', { method: 'POST' });
      const result = await res.json();
      if (result.success) {
        showToast('Arquivos originais restaurados com sucesso!', 'success');
        fetchStatus();
      } else {
        throw new Error(result.error || 'Erro ao restaurar arquivos.');
      }
    } catch (err) {
      showToast(err.message, 'error');
      fetchStatus();
    }
  });

  // Iniciar jogo
  btnLaunch.addEventListener('click', async () => {
    try {
      showToast('Iniciando o jogo Dressmaker...', 'info');
      await fetch('/api/launch', { method: 'POST' });
    } catch (err) {
      showToast('Erro ao iniciar o executável do jogo.', 'error');
    }
  });

  // Polling suave a cada 5 segundos para detectar se o jogo foi aberto/fechado
  setInterval(fetchStatus, 5000);

  // Inicialização imediata
  fetchStatus();
});
