@echo off
REM -- Este script inicia a interface gráfica (GUI)
REM -- O comando 'start' impede que o terminal fique bloqueado pela GUI.
echo Iniciando o Painel de Configurações...
start "" C:\Python38\python.exe "services\settings_gui.py"

REM -- A linha abaixo fecha o terminal automaticamente após iniciar o programa
exit