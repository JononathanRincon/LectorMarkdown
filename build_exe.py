"""
Build script for compiling LectorMarkdown into a standalone Windows .exe using PyInstaller.
Produces a clean, single-file executable with no console window and custom icon.
"""
import os
import sys
import subprocess

def build():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, "assets", "icon.ico")
    main_py = os.path.join(base_dir, "main.py")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=LectorMarkdown",
        "--noconsole",
        "--onefile",
        "--clean",
        f"--icon={icon_path}",
        f"--add-data=assets{os.pathsep}assets",
        "--hidden-import=markdown_it",
        "--hidden-import=mdit_py_plugins",
        "--hidden-import=mdit_py_plugins.tasklists",
        "--hidden-import=linkify_it",
        "--hidden-import=pygments",
        "--hidden-import=pygments.lexers",
        "--hidden-import=pygments.formatters",
        "--hidden-import=pygments.styles",
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        main_py
    ]

    print("Executing PyInstaller build...")
    print(" ".join(cmd))
    result = subprocess.run(cmd, cwd=base_dir)

    if result.returncode == 0:
        exe_path = os.path.join(base_dir, "dist", "LectorMarkdown.exe")
        print("=" * 60)
        print("BUILD SUCCESSFUL!")
        print(f"Executable created at: {exe_path}")
        print("=" * 60)
        return True
    else:
        print("=" * 60)
        print("BUILD FAILED with exit code", result.returncode)
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
