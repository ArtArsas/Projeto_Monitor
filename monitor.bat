@echo off
REM -- Executa o programa monitor.py
REM -- O comando 'cls' limpa o console para uma inicialização limpa.
cls

REM -- Verifica se o Python está no PATH e executa o script principal.
REM -- O comando 'python' (ou 'py') deve ser usado aqui. Usaremos 'py' que é mais confiável.
echo Iniciando Monitor Parental Inteligente...
echo.
py "teste_input_condition.py"

REM -- Pausa no final para que o usuário possa ler a mensagem de encerramento,
REM -- caso o script Python termine por acidente.
pause