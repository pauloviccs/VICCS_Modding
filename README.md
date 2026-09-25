# Dressmaker — Mod de Tradução PT-BR & Instalador Plug-and-Play

Mod de localização completo para Português do Brasil do jogo **Dressmaker**, acompanhado de um instalador desktop nativo e ultraleve com estética refinada *Cozy Atelier*.

---

## 🪡 Destaques do Projeto

- **Arquitetura Plug-and-Play:** Patch cirúrgico direto nos pacotes de idioma UnityFS (Addressables/Unity Localization).
- **Sem Injeção de DLLs ou Hacks Frágeis:** Não depende de BepInEx nem modifica a memória do executável.
- **Backup & Restauração em 1 Clique:** Criação automática de cópia de segurança antes de aplicar qualquer alteração.
- **Interface Cozy & Premium:** Desenvolvida com glassmorphism, paleta quente de veludo e dourado, tipografia cinematográfica e micro-animações de costura.
- **Detecção Automática:** Localiza automaticamente a instalação do jogo em `C:\Games\Dressmaker` ou bibliotecas Steam.

---

## 🚀 Como Executar o Instalador

Basta dar dois cliques em:
```text
Iniciar_Instalador.bat
```
Ou executar diretamente via terminal:
```bash
python run_installer.py
```

---

## 📂 Estrutura de Diretórios

```text
├── data/
│   ├── raw_strings_en.json         # Strings originais extraídas (~5886 itens)
│   └── translations_ptbr.json      # Strings traduzidas em PT-BR (menus, tutoriais, itens)
├── src/
│   ├── backend/
│   │   ├── engine_inspector.py     # Extrator de tabelas Unity Localization
│   │   ├── patcher.py              # Motor de backup, validação e aplicação do mod
│   │   └── server.py               # Servidor local ultraleve com API REST
│   └── frontend/
│       ├── index.html              # Interface do usuário (Cozy Atelier)
│       ├── styles.css              # Design tokens, animações e glassmorphism
│       └── app.js                  # Controle reativo de estado e feedback visual
├── tools/
│   └── build_translations.py       # Script de compilação e mapeamento de traduções
├── run_installer.py                # Inicializador com janela nativa WebView2
└── Iniciar_Instalador.bat          # Atalho para o usuário final
```
