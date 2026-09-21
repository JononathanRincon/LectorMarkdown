@echo off
chcp 65001 >nul
title Lector Markdown - Eliminar integracion de Windows
echo =======================================================
echo    Eliminando Lector Markdown de Windows Explorer
echo =======================================================
echo.
echo Eliminando menu contextual y asociacion de archivos .md...
echo.

python -c "import sys; sys.path.insert(0, '.'); from core.windows_registry import unregister_windows_integration; ok, msg = unregister_windows_integration(); print(msg); sys.exit(0 if ok else 1)"

if %ERRORLEVEL% equ 0 (
    echo.
    echo [EXITO] Se ha eliminado la asociacion de Windows correctamente.
) else (
    echo.
    echo [ERROR] Ocurrio un error al desinstalar la asociacion.
)

echo.
pause
