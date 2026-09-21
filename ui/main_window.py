"""
Main Window for LectorMarkdown.
Manages application lifecycle, toolbar actions, reading/editing view switching,
search bar, file persistence, drag-and-drop, and Windows integration dialog.
"""
import os
import sys
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QToolBar,
    QStatusBar, QLabel, QFileDialog, QMessageBox, QDialog,
    QHBoxLayout, QPushButton, QGroupBox
)
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QDragEnterEvent, QDropEvent, QTextDocument

from config import config
from core.file_manager import FileManager
from core.windows_registry import (
    is_context_menu_registered, is_file_association_registered,
    register_windows_integration, unregister_windows_integration
)
from ui.reader_view import ReaderView
from ui.editor_view import EditorView
from ui.search_bar import SearchBar
from ui.styles import get_app_qss
from ui.resources import (
    get_pencil_icon, get_save_icon, get_reader_icon,
    get_folder_icon, get_sun_icon, get_moon_icon,
    get_search_icon, get_zoom_in_icon, get_zoom_out_icon,
    get_windows_icon
)

class WindowsIntegrationDialog(QDialog):
    """Dialog to easily configure or remove Windows Explorer integration."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Integración con Windows")
        self.setFixedSize(480, 260)
        self._setup_ui()
        self._update_status()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        group = QGroupBox("Estado de la Integración en el Explorador de Windows")
        g_layout = QVBoxLayout(group)
        g_layout.setSpacing(8)

        self.lbl_context = QLabel()
        self.lbl_context.setWordWrap(True)
        g_layout.addWidget(self.lbl_context)

        self.lbl_assoc = QLabel()
        self.lbl_assoc.setWordWrap(True)
        g_layout.addWidget(self.lbl_assoc)

        layout.addWidget(group)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_install = QPushButton("Activar Integración")
        self.btn_install.setStyleSheet("background-color: #2563eb; color: white; padding: 7px 14px; font-weight: bold; border-radius: 4px;")
        self.btn_install.clicked.connect(self._install_integration)
        btn_layout.addWidget(self.btn_install)

        self.btn_uninstall = QPushButton("Desinstalar Integración")
        self.btn_uninstall.setStyleSheet("background-color: #dc2626; color: white; padding: 7px 14px; font-weight: bold; border-radius: 4px;")
        self.btn_uninstall.clicked.connect(self._uninstall_integration)
        btn_layout.addWidget(self.btn_uninstall)

        layout.addLayout(btn_layout)

        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def _update_status(self):
        ctx_ok = is_context_menu_registered()
        assoc_ok = is_file_association_registered()

        ctx_text = "✅ <b>Menú contextual:</b> Activo ('Abrir con Lector Markdown')" if ctx_ok else "⚠️ <b>Menú contextual:</b> No registrado"
        assoc_text = "✅ <b>Asociación .md:</b> Lector Markdown es el programa predeterminado" if assoc_ok else "⚠️ <b>Asociación .md:</b> No es el visor predeterminado"

        self.lbl_context.setText(ctx_text)
        self.lbl_assoc.setText(assoc_text)

        self.btn_install.setEnabled(not (ctx_ok and assoc_ok))
        self.btn_uninstall.setEnabled(ctx_ok or assoc_ok)

    def _install_integration(self):
        ok, msg = register_windows_integration()
        if ok:
            QMessageBox.information(self, "Integración Registrada", msg)
        else:
            QMessageBox.warning(self, "Error de Integración", msg)
        self._update_status()

    def _uninstall_integration(self):
        ok, msg = unregister_windows_integration()
        if ok:
            QMessageBox.information(self, "Integración Desinstalada", msg)
        else:
            QMessageBox.warning(self, "Error", msg)
        self._update_status()


class MainWindow(QMainWindow):
    def __init__(self, initial_file: Optional[str] = None):
        super().__init__()
        self.file_manager = FileManager()
        self.current_theme = config.theme or "light"
        
        # Set app icon if available
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        icon_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setAcceptDrops(True)
        self._setup_ui()
        self.apply_theme(self.current_theme)

        # Restore window geometry
        geom = config.window_geometry
        if geom:
            self.restoreGeometry(geom)
        else:
            self.resize(1000, 750)

        # Center window if first time
        if not geom:
            qr = self.frameGeometry()
            cp = self.screen().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

        # Load initial file or show empty state
        if initial_file and os.path.exists(initial_file):
            self.open_file_path(initial_file)
        else:
            self.show_empty_state()

    def _setup_ui(self):
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_statusbar()
        self._setup_shortcuts()

    def _setup_toolbar(self):
        self.toolbar = QToolBar("Barra Principal")
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Open File Action
        self.action_open = QAction(get_folder_icon(), " Abrir Archivo", self)
        self.action_open.setToolTip("Abrir archivo Markdown (Ctrl+O)")
        self.action_open.triggered.connect(self.prompt_open_file)
        self.toolbar.addAction(self.action_open)

        self.toolbar.addSeparator()

        # EDIT Action (Pencil ✏️)
        self.action_edit = QAction(get_pencil_icon(), " Editar (✏️)", self)
        self.action_edit.setToolTip("Editar archivo Markdown (Ctrl+E)")
        self.action_edit.triggered.connect(self.switch_to_editor_mode)
        self.toolbar.addAction(self.action_edit)

        # SAVE Action (💾)
        self.action_save = QAction(get_save_icon(), " Guardar (💾)", self)
        self.action_save.setToolTip("Guardar cambios y volver a lectura (Ctrl+S)")
        self.action_save.triggered.connect(self.save_and_return_to_reading)
        self.toolbar.addAction(self.action_save)
        self.action_save.setVisible(False)  # Hidden in reading mode

        # RETURN TO READING Action (👁️)
        self.action_read = QAction(get_reader_icon(), " Vista Lectura (👁️)", self)
        self.action_read.setToolTip("Volver al modo de lectura (Esc / Ctrl+R)")
        self.action_read.triggered.connect(self.switch_to_reading_mode)
        self.toolbar.addAction(self.action_read)
        self.action_read.setVisible(False)

        self.toolbar.addSeparator()

        # THEME TOGGLE
        theme_icon = get_moon_icon() if self.current_theme == "light" else get_sun_icon()
        self.action_theme = QAction(theme_icon, " Tema", self)
        self.action_theme.setToolTip("Alternar entre Tema Claro y Oscuro")
        self.action_theme.triggered.connect(self.toggle_theme)
        self.toolbar.addAction(self.action_theme)

        # SEARCH Action (🔍)
        self.action_search = QAction(get_search_icon(), " Buscar", self)
        self.action_search.setToolTip("Buscar en el texto (Ctrl+F)")
        self.action_search.triggered.connect(self.toggle_search)
        self.toolbar.addAction(self.action_search)

        self.toolbar.addSeparator()

        # ZOOM Actions
        self.action_zoom_in = QAction(get_zoom_in_icon(), "", self)
        self.action_zoom_in.setToolTip("Aumentar tamaño de texto (Ctrl++)")
        self.action_zoom_in.triggered.connect(self._zoom_in)
        self.toolbar.addAction(self.action_zoom_in)

        self.action_zoom_out = QAction(get_zoom_out_icon(), "", self)
        self.action_zoom_out.setToolTip("Reducir tamaño de texto (Ctrl+-)")
        self.action_zoom_out.triggered.connect(self._zoom_out)
        self.toolbar.addAction(self.action_zoom_out)

        self.toolbar.addSeparator()

        # WINDOWS INTEGRATION Action
        self.action_windows = QAction(get_windows_icon(), " Integración Windows", self)
        self.action_windows.setToolTip("Configurar 'Abrir con Lector Markdown' en el Explorador de Windows")
        self.action_windows.triggered.connect(self.open_windows_integration_dialog)
        self.toolbar.addAction(self.action_windows)

    def _setup_central_widget(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Search Bar
        self.search_bar = SearchBar(self)
        self.search_bar.find_next_requested.connect(self._handle_search_next)
        self.search_bar.find_prev_requested.connect(self._handle_search_prev)
        layout.addWidget(self.search_bar)

        # Stacked Widget: [0] ReaderView, [1] EditorView
        self.stack = QStackedWidget()
        
        self.reader_view = ReaderView(self)
        self.reader_view.link_open_requested.connect(self._handle_local_link)
        self.stack.addWidget(self.reader_view)

        self.editor_view = EditorView(self)
        self.editor_view.cursor_info_changed.connect(self._handle_cursor_changed)
        self.editor_view.textChanged.connect(self._handle_editor_text_changed)
        self.stack.addWidget(self.editor_view)

        layout.addWidget(self.stack)
        self.setCentralWidget(container)

    def _setup_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_mode = QLabel("Modo Lectura")
        self.status_mode.setStyleSheet("font-weight: bold; color: #3b82f6;")
        self.status_bar.addWidget(self.status_mode)

        self.status_file = QLabel("Sin archivo abierto")
        self.status_bar.addWidget(self.status_file, 1)

        self.status_stats = QLabel("")
        self.status_bar.addPermanentWidget(self.status_stats)

        self.status_encoding = QLabel("UTF-8")
        self.status_bar.addPermanentWidget(self.status_encoding)

    def _setup_shortcuts(self):
        # Ctrl+O: Open
        self.action_open.setShortcut(QKeySequence.StandardKey.Open)
        # Ctrl+S: Save
        self.action_save.setShortcut(QKeySequence.StandardKey.Save)
        # Ctrl+F: Search
        self.action_search.setShortcut(QKeySequence.StandardKey.Find)
        # Ctrl+E: Edit
        self.action_edit.setShortcut(QKeySequence("Ctrl+E"))
        # Esc: Return to reading or close search
        # Zoom shortcuts
        self.action_zoom_in.setShortcut(QKeySequence.StandardKey.ZoomIn)
        self.action_zoom_out.setShortcut(QKeySequence.StandardKey.ZoomOut)

    # ------------------ Themes ------------------ #
    def apply_theme(self, theme: str):
        self.current_theme = theme
        config.theme = theme
        
        # Apply Application QSS
        qss = get_app_qss(theme)
        self.setStyleSheet(qss)

        # Update Views
        self.reader_view.update_theme(theme)
        self.editor_view.set_theme(theme)

        # Update Theme Button Icon
        if theme == "dark":
            self.action_theme.setIcon(get_sun_icon())
            self.action_theme.setText(" Tema Claro")
            self.status_mode.setStyleSheet("font-weight: bold; color: #89b4fa;")
        else:
            self.action_theme.setIcon(get_moon_icon())
            self.action_theme.setText(" Tema Oscuro")
            self.status_mode.setStyleSheet("font-weight: bold; color: #2563eb;")

    def toggle_theme(self):
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)

    # ------------------ Mode Switching ------------------ #
    def switch_to_editor_mode(self):
        """Switches view to the Markdown plain text editor."""
        # Transfer current markdown text to editor
        content = self.file_manager.current_content
        self.editor_view.setPlainText(content)
        self.file_manager.set_modified(False, content)

        self.stack.setCurrentIndex(1)
        self.editor_view.setFocus()

        # Update Toolbar
        self.action_edit.setVisible(False)
        self.action_save.setVisible(True)
        self.action_read.setVisible(True)

        # Update Status Bar
        self.status_mode.setText("Modo Edición")
        self._update_title()
        self._update_stats()

    def switch_to_reading_mode(self, check_dirty: bool = True):
        """Switches view back to clean Markdown reading mode."""
        if check_dirty and self.file_manager.is_modified:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                "Tienes modificaciones sin guardar en el archivo.\n¿Deseas guardarlas antes de volver a la vista de lectura?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_and_return_to_reading()
                return
            elif reply == QMessageBox.StandardButton.Cancel:
                return
            # If Discard: revert changes
            self.file_manager.current_content = self.file_manager.original_content
            self.file_manager.set_modified(False)

        # Render clean HTML
        self.reader_view.set_markdown_content(self.file_manager.current_content, theme=self.current_theme)
        self.stack.setCurrentIndex(0)

        # Update Toolbar
        self.action_edit.setVisible(True)
        self.action_save.setVisible(False)
        self.action_read.setVisible(False)

        # Update Status Bar
        self.status_mode.setText("Modo Lectura")
        self._update_title()
        self._update_stats()

    def save_and_return_to_reading(self):
        """Saves editor changes to file and switches back to Reading Mode."""
        new_content = self.editor_view.toPlainText()

        if not self.file_manager.has_file:
            # Prompt Save As
            target_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo Markdown",
                os.path.join(self.file_manager.directory, self.file_manager.filename),
                "Archivos Markdown (*.md *.markdown);;Todos los archivos (*.*)"
            )
            if not target_path:
                return
            self.file_manager.file_path = target_path

        ok, msg = self.file_manager.save_file(new_content)
        if ok:
            self.status_bar.showMessage(msg, 4000)
            config.add_recent_file(self.file_manager.file_path)
            # Switch back to reading mode
            self.switch_to_reading_mode(check_dirty=False)
        else:
            QMessageBox.critical(self, "Error al guardar", msg)

    # ------------------ File Operations ------------------ #
    def prompt_open_file(self):
        start_dir = self.file_manager.directory
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo Markdown",
            start_dir,
            "Archivos Markdown (*.md *.markdown *.mdown *.mkd);;Todos los archivos (*.*)"
        )
        if path:
            self.open_file_path(path)

    def open_file_path(self, path: str):
        if self.file_manager.is_modified:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                "El documento actual tiene cambios sin guardar.\n¿Deseas descartarlos para abrir el nuevo archivo?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        ok, content_or_err, encoding = self.file_manager.load_file(path)
        if not ok:
            QMessageBox.critical(self, "Error al abrir archivo", content_or_err)
            return

        config.add_recent_file(self.file_manager.file_path)

        # Show in Reading Mode
        self.reader_view.set_markdown_content(content_or_err, theme=self.current_theme)
        self.stack.setCurrentIndex(0)
        self.action_edit.setVisible(True)
        self.action_save.setVisible(False)
        self.action_read.setVisible(False)
        self.status_mode.setText("Modo Lectura")

        self._update_title()
        self._update_stats()
        self.status_file.setText(self.file_manager.file_path)
        self.status_encoding.setText(encoding.upper())
        self.status_bar.showMessage(f"Archivo cargado: {self.file_manager.filename}", 3500)

    def show_empty_state(self):
        welcome_md = """# 👋 ¡Bienvenido a Lector Markdown!

Lector Markdown es tu visor y editor minimalista para Windows.
Lee cualquier archivo Markdown convertido a una lectura visual limpia y elegante, sin etiquetas de sintaxis visibles.

### ✨ Funciones principales:
- **Lectura Limpia:** Encabezados estilizados, tablas GFM, listas de tareas y código con resaltado sintáctico.
- **Edición Rápida (✏️):** Pulsa el botón de **Editar (✏️)** en la barra de herramientas para modificar el contenido y **Guardar (💾)** con `Ctrl+S`.
- **Temas:** Alterna en cualquier momento entre **Tema Claro** y **Tema Oscuro** (☀️/🌙).
- **Integración con Windows:** Clic derecho en cualquier archivo `.md` en el Explorador de Windows y selecciona **"Abrir con Lector Markdown"**.

---
> [!TIP]
> Puedes arrastrar y soltar cualquier archivo `.md` directamente en esta ventana para abrirlo al instante.
"""
        self.file_manager.original_content = welcome_md
        self.file_manager.current_content = welcome_md
        self.file_manager.file_path = None
        self.reader_view.set_markdown_content(welcome_md, theme=self.current_theme)
        self.stack.setCurrentIndex(0)
        self.status_file.setText("Documento de bienvenida")
        self._update_title()
        self._update_stats()

    def _handle_local_link(self, link_str: str):
        """Resolves clicked relative markdown links."""
        if not self.file_manager.has_file:
            return
        base_dir = self.file_manager.directory
        clean_path = link_str.split("#")[0]
        target_path = os.path.normpath(os.path.join(base_dir, clean_path))
        if os.path.exists(target_path):
            self.open_file_path(target_path)

    # ------------------ Search Operations ------------------ #
    def toggle_search(self):
        if self.search_bar.isVisible():
            self.search_bar.hide_search()
        else:
            self.search_bar.show_search()

    def _handle_search_next(self, query: str, case_sensitive: bool):
        flags = QTextDocument.FindFlag(0)
        if case_sensitive:
            flags |= QTextDocument.FindFlag.FindCaseSensitively

        target_widget = self.reader_view if self.stack.currentIndex() == 0 else self.editor_view
        found = target_widget.find(query, flags)
        if not found:
            # Wrap around: move cursor to start and try again
            target_widget.moveCursor(target_widget.textCursor().MoveOperation.Start)
            found = target_widget.find(query, flags)
            if not found:
                self.status_bar.showMessage(f"No se encontró: '{query}'", 2500)

    def _handle_search_prev(self, query: str, case_sensitive: bool):
        flags = QTextDocument.FindFlag.FindBackward
        if case_sensitive:
            flags |= QTextDocument.FindFlag.FindCaseSensitively

        target_widget = self.reader_view if self.stack.currentIndex() == 0 else self.editor_view
        found = target_widget.find(query, flags)
        if not found:
            target_widget.moveCursor(target_widget.textCursor().MoveOperation.End)
            found = target_widget.find(query, flags)
            if not found:
                self.status_bar.showMessage(f"No se encontró: '{query}'", 2500)

    # ------------------ Zoom Helpers ------------------ #
    def _zoom_in(self):
        if self.stack.currentIndex() == 0:
            self.reader_view.zoom_in()
        else:
            self.editor_view.zoomIn(1)

    def _zoom_out(self):
        if self.stack.currentIndex() == 0:
            self.reader_view.zoom_out()
        else:
            self.editor_view.zoomOut(1)

    # ------------------ State & Helpers ------------------ #
    def _handle_editor_text_changed(self):
        if self.stack.currentIndex() == 1:
            is_modified = (self.editor_view.toPlainText() != self.file_manager.original_content)
            self.file_manager.set_modified(is_modified, self.editor_view.toPlainText())
            self._update_title()
            self._update_stats(self.editor_view.toPlainText())

    def _handle_cursor_changed(self, line: int, col: int):
        if self.stack.currentIndex() == 1:
            self.status_mode.setText(f"Modo Edición | Ln {line}, Col {col}")

    def _update_title(self):
        star = " *" if self.file_manager.is_modified else ""
        name = self.file_manager.filename
        self.setWindowTitle(f"{name}{star} - Lector Markdown")

    def _update_stats(self, text: Optional[str] = None):
        stats = self.file_manager.get_stats(text)
        mins = stats["reading_minutes"]
        words = stats["words"]
        chars = stats["characters"]
        time_str = f"~{mins} min de lectura" if mins > 0 else "< 1 min"
        self.status_stats.setText(f"{words:,} palabras | {chars:,} caracteres | {time_str}")

    def open_windows_integration_dialog(self):
        dialog = WindowsIntegrationDialog(self)
        dialog.exec()

    # ------------------ Drag & Drop ------------------ #
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for u in urls:
                if u.toLocalFile().lower().endswith((".md", ".markdown", ".mdown", ".txt")):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        for u in urls:
            path = u.toLocalFile()
            if path and os.path.exists(path):
                self.open_file_path(path)
                event.acceptProposedAction()
                return

    # ------------------ Window Close ------------------ #
    def closeEvent(self, event):
        if self.file_manager.is_modified:
            reply = QMessageBox.question(
                self,
                "Guardar cambios",
                f"¿Deseas guardar los cambios realizados en {self.file_manager.filename} antes de salir?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_and_return_to_reading()
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return

        # Save window geometry
        config.window_geometry = self.saveGeometry()
        event.accept()
