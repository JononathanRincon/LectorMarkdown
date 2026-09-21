@echo off
chcp 65001 >nul
title Lector Markdown - Registrar en Windows
echo =======================================================
echo    Configurando Lector Markdown en Windows Explorer
echo =======================================================
echo.
echo 1. Agregando opcion "Abrir con Lector Markdown" al menu contextual...
echo 2. Estableciendo asociacion predeterminada para archivos .md...
echo.

python -c "import sys; sys.path.insert(0, '.'); from core.windows_registry import register_windows_integration; ok, msg = register_windows_integration(); print(msg); sys.exit(0 if ok else 1)"

if %ERRORLEVEL% equ 0 (
    echo.
    echo [EXITO] La integracion con Windows se ha completado correctamente.
    echo Ahora puedes hacer clic derecho en cualquier archivo .md y seleccionar
    echo "Abrir con Lector Markdown" o abrirlo con doble clic.
) else (
    echo.
    echo [ERROR] Ocurrio un error al registrar la asociacion.
)

echo.
pause
