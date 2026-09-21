"""
Search bar widget for LectorMarkdown.
Provides in-document text search with Next, Previous, Case sensitivity, and Esc to close.
"""
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut

class SearchBar(QFrame):
    find_next_requested = pyqtSignal(str, bool)  # text, case_sensitive
    find_prev_requested = pyqtSignal(str, bool)  # text, case_sensitive
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("searchFrame")
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        self.label = QLabel("Buscar:")
        layout.addWidget(self.label)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Escribe para buscar... (Presiona Enter para siguiente)")
        self.search_input.returnPressed.connect(self._on_search_next)
        layout.addWidget(self.search_input)

        self.btn_prev = QPushButton("▲ Anterior")
        self.btn_prev.setObjectName("searchButton")
        self.btn_prev.setToolTip("Buscar anterior (Shift+F3)")
        self.btn_prev.clicked.connect(self._on_search_prev)
        layout.addWidget(self.btn_prev)

        self.btn_next = QPushButton("▼ Siguiente")
        self.btn_next.setObjectName("searchButton")
        self.btn_next.setToolTip("Buscar siguiente (F3 o Enter)")
        self.btn_next.clicked.connect(self._on_search_next)
        layout.addWidget(self.btn_next)

        self.case_check = QCheckBox("Mayúsculas/minúsculas")
        layout.addWidget(self.case_check)

        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("searchButton")
        self.btn_close.setToolTip("Cerrar búsqueda (Esc)")
        self.btn_close.setFixedWidth(28)
        self.btn_close.clicked.connect(self.hide_search)
        layout.addWidget(self.btn_close)

        # Shortcuts
        self.shortcut_esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.shortcut_esc.activated.connect(self.hide_search)

        self.shortcut_f3 = QShortcut(QKeySequence(Qt.Key.Key_F3), self)
        self.shortcut_f3.activated.connect(self._on_search_next)

        self.shortcut_shift_f3 = QShortcut(QKeySequence("Shift+F3"), self)
        self.shortcut_shift_f3.activated.connect(self._on_search_prev)

        self.hide()

    def show_search(self):
        self.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def hide_search(self):
        self.hide()
        self.closed.emit()

    def _on_search_next(self):
        text = self.search_input.text()
        if text:
            self.find_next_requested.emit(text, self.case_check.isChecked())

    def _on_search_prev(self):
        text = self.search_input.text()
        if text:
            self.find_prev_requested.emit(text, self.case_check.isChecked())
