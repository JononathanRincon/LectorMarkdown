"""
Windows Registry module for LectorMarkdown.
Manages Windows Explorer context menu integration ('Abrir con Lector Markdown')
and .md file extension association under HKEY_CURRENT_USER without requiring admin privileges.
"""
import sys
import os
import winreg
from typing import Tuple, Optional

PROG_ID = "LectorMarkdown.File"
APP_NAME = "Lector Markdown"
MENU_TEXT = "Abrir con Lector Markdown"
EXTENSION = ".md"

def get_executable_command() -> Tuple[str, str]:
    """
    Returns (command_string, icon_path) for registering in Windows.
    Handles both frozen PyInstaller .exe and standard Python script execution (using pythonw).
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    icon_path = os.path.join(base_dir, "assets", "icon.ico")
    
    if not os.path.exists(icon_path):
        icon_path = sys.executable

    if getattr(sys, "frozen", False):
        # Compiled executable
        exe_path = sys.executable
        command = f'"{exe_path}" "%1"'
        return command, exe_path
    else:
        # Check if compiled binary exists in dist/
        dist_exe = os.path.join(base_dir, "dist", "LectorMarkdown.exe")
        if os.path.exists(dist_exe):
            command = f'"{dist_exe}" "%1"'
            return command, dist_exe

        # Running from Python source
        # Prefer pythonw.exe to prevent black console window
        python_dir = os.path.dirname(sys.executable)
        pythonw_path = os.path.join(python_dir, "pythonw.exe")
        if not os.path.exists(pythonw_path):
            pythonw_path = sys.executable

        main_py = os.path.join(base_dir, "main.py")
        command = f'"{pythonw_path}" "{main_py}" "%1"'
        return command, icon_path

def is_context_menu_registered() -> bool:
    """Checks if the context menu 'Abrir con Lector Markdown' is currently registered."""
    key_path = f"Software\\Classes\\SystemFileAssociations\\{EXTENSION}\\shell\\LectorMarkdown"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ):
            return True
    except OSError:
        return False

def is_file_association_registered() -> bool:
    """Checks if .md extension is associated with LectorMarkdown.File."""
    key_path = f"Software\\Classes\\{EXTENSION}"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
            val = winreg.QueryValue(key, "")
            return val == PROG_ID
    except OSError:
        return False

def register_windows_integration() -> Tuple[bool, str]:
    """
    Registers both:
    1. Windows Explorer right-click context menu ('Abrir con Lector Markdown').
    2. Default file association for .md files.
    All inside HKEY_CURRENT_USER (no Administrator privileges needed).
    """
    command, icon_path = get_executable_command()

    try:
        # 1. Register Context Menu for .md in SystemFileAssociations
        assoc_key_path = f"Software\\Classes\\SystemFileAssociations\\{EXTENSION}\\shell\\LectorMarkdown"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, assoc_key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, MENU_TEXT)
            if icon_path:
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, f'"{icon_path}"')

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{assoc_key_path}\\command") as cmd_key:
            winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, command)

        # 2. Register ProgID for LectorMarkdown.File
        prog_path = f"Software\\Classes\\{PROG_ID}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_path) as prog_key:
            winreg.SetValueEx(prog_key, "", 0, winreg.REG_SZ, "Documento Markdown")

        # Set Icon for ProgID
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{prog_path}\\DefaultIcon") as icon_key:
            winreg.SetValueEx(icon_key, "", 0, winreg.REG_SZ, f'"{icon_path}",0')

        # Set Open command for ProgID
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{prog_path}\\shell\\open\\command") as open_key:
            winreg.SetValueEx(open_key, "", 0, winreg.REG_SZ, command)

        # 3. Associate .md extension with ProgID in HKCU
        ext_path = f"Software\\Classes\\{EXTENSION}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_path) as ext_key:
            winreg.SetValueEx(ext_key, "", 0, winreg.REG_SZ, PROG_ID)

        # Tell Windows Explorer to refresh its icon & association cache
        _notify_shell_change()

        return True, "Integración en Windows registrada con éxito (Menú contextual y asociación .md)."
    except Exception as e:
        return False, f"Error al registrar en Windows: {str(e)}"

def _delete_key_tree(root, subkey):
    """Recursively deletes a Windows registry key and all subkeys."""
    try:
        with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
            while True:
                try:
                    sub = winreg.EnumKey(key, 0)
                    _delete_key_tree(root, f"{subkey}\\{sub}")
                except OSError:
                    break
        winreg.DeleteKey(root, subkey)
    except OSError:
        pass

def unregister_windows_integration() -> Tuple[bool, str]:
    """
    Removes the context menu and .md file association from HKEY_CURRENT_USER.
    """
    try:
        # Delete SystemFileAssociations context menu
        _delete_key_tree(
            winreg.HKEY_CURRENT_USER,
            f"Software\\Classes\\SystemFileAssociations\\{EXTENSION}\\shell\\LectorMarkdown"
        )

        # Delete ProgID
        _delete_key_tree(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{PROG_ID}")

        # Remove default from .md if it points to PROG_ID
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{EXTENSION}", 0, winreg.KEY_ALL_ACCESS) as ext_key:
                val = winreg.QueryValue(ext_key, "")
                if val == PROG_ID:
                    winreg.DeleteValue(ext_key, "")
        except OSError:
            pass

        _notify_shell_change()
        return True, "Integración en Windows desinstalada correctamente."
    except Exception as e:
        return False, f"Error al desinstalar integración: {str(e)}"

def _notify_shell_change():
    """Notifies Windows Shell (Explorer) that file associations have changed."""
    try:
        import ctypes
        SHCNE_ASSOCCHANGED = 0x08000000
        SHCNF_IDLIST = 0x0000
        ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
    except Exception:
        pass
