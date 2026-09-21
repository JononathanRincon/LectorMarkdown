"""
LectorMarkdown - Aplicación de escritorio para Windows.
Visor minimalista y editor de archivos Markdown (.md) con lectura limpia sin sintaxis visible.
"""
import sys
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow

def main():
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Lector Markdown")
    app.setApplicationDisplayName("Lector Markdown")
    app.setOrganizationName("LectorMarkdown")

    # Set application icon
    base_dir = os.path.abspath(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Check if a file argument was passed (e.g. from Windows Explorer "Abrir con..." or double click)
    initial_file = None
    if len(sys.argv) > 1:
        arg_path = sys.argv[1].strip('"')
        if os.path.exists(arg_path):
            initial_file = os.path.abspath(arg_path)

    window = MainWindow(initial_file=initial_file)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
