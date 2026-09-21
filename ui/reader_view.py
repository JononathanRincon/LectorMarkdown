"""
Reader view component for LectorMarkdown.
Renders markdown content converted to clean HTML without any raw markdown tags.
Supports external links, internal anchors, zooming, and smooth reading.
"""
from typing import Optional
from PyQt6.QtWidgets import QTextBrowser
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QDesktopServices, QTextDocument, QTextCursor

class ReaderView(QTextBrowser):
    link_open_requested = pyqtSignal(str)
    zoom_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        self.anchorClicked.connect(self._handle_anchor_click)
        
        self.setReadOnly(True)
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self._zoom_level = 0
        self._last_markdown = ""
        self._current_theme = "light"

    def set_markdown_content(self, markdown_text: str, theme: str = "light"):
        """Renders markdown text as clean HTML preserving scroll position if possible."""
        from core.markdown_parser import markdown_to_html
        
        self._last_markdown = markdown_text
        self._current_theme = theme
        
        # Save scroll position
        scrollbar = self.verticalScrollBar()
        current_scroll = scrollbar.value() if scrollbar else 0
        
        html = markdown_to_html(markdown_text, theme=theme)
        self.setHtml(html)
        
        if scrollbar and current_scroll > 0:
            scrollbar.setValue(current_scroll)

    def update_theme(self, theme: str):
        """Updates the theme and re-renders current content."""
        if self._last_markdown:
            self.set_markdown_content(self._last_markdown, theme)

    def _handle_anchor_click(self, url: QUrl):
        """Handles link clicks: external URLs in default browser, local .md files in reader."""
        url_str = url.toString()
        if url_str.startswith("#"):
            # Internal anchor
            anchor_name = url_str[1:]
            self.scrollToAnchor(anchor_name)
        elif url_str.startswith("http://") or url_str.startswith("https://") or url_str.startswith("mailto:"):
            QDesktopServices.openUrl(url)
        elif url_str.endswith(".md") or ".md#" in url_str:
            self.link_open_requested.emit(url_str)
        else:
            QDesktopServices.openUrl(url)

    def zoom_in(self):
        if self._zoom_level < 10:
            self._zoom_level += 1
            self.zoomIn(1)
            self.zoom_changed.emit(self._zoom_level)

    def zoom_out(self):
        if self._zoom_level > -5:
            self._zoom_level -= 1
            self.zoomOut(1)
            self.zoom_changed.emit(self._zoom_level)

    def reset_zoom(self):
        if self._zoom_level != 0:
            self.zoomOut(self._zoom_level) if self._zoom_level > 0 else self.zoomIn(abs(self._zoom_level))
            self._zoom_level = 0
            self.zoom_changed.emit(0)

    def wheelEvent(self, event):
        """Allow Ctrl + Wheel to zoom in/out."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            elif delta < 0:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)
