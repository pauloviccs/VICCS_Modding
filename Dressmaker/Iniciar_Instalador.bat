@echo off
title Dressmaker - Traducao PT-BR (Instalador)
echo Verificando dependencias necessarias (UnityPy)...
python -c "import UnityPy" 2>nul || (
    echo Instalando UnityPy para manipulacao dos arquivos da Unity...
    pip install UnityPy
)
echo Iniciando o Atelie de Localizacao Dressmaker PT-BR...
python run_installer.py
pause
