"""
Editor view component for LectorMarkdown.
Modern plain text editor with line numbers, monospace font, indentation helpers, and theme support.
"""
from PyQt6.QtWidgets import QPlainTextEdit, QWidget
from PyQt6.QtGui import QPainter, QColor, QTextFormat, QFont, QTextCursor, QKeyEvent
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal

class LineNumberArea(QWidget):
    def __init__(self, editor: "EditorView"):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class EditorView(QPlainTextEdit):
    cursor_info_changed = pyqtSignal(int, int)  # line, col

    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self._handle_cursor_changed)

        self._theme = "light"
        self._setup_editor()
        self.updateLineNumberAreaWidth(0)

    def _setup_editor(self):
        font = QFont("Cascadia Code")
        if not font.exactMatch():
            font = QFont("Consolas")
        font.setPointSize(11)
        self.setFont(font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)

    def set_theme(self, theme: str):
        self._theme = theme
        self.line_number_area.update()

    def lineNumberAreaWidth(self) -> int:
        digits = max(1, len(str(self.blockCount())))
        space = 18 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        
        # Colors depending on theme
        if self._theme == "dark":
            bg_color = QColor("#11111b")
            num_color = QColor("#585b70")
            current_num_color = QColor("#cdd6f4")
        else:
            bg_color = QColor("#f8fafc")
            num_color = QColor("#94a3b8")
            current_num_color = QColor("#0f172a")

        painter.fillRect(event.rect(), bg_color)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        current_block = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number_str = str(block_number + 1)
                is_current = (block_number == current_block)
                painter.setPen(current_num_color if is_current else num_color)
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width() - 8,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number_str
                )

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def _handle_cursor_changed(self):
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.positionInBlock() + 1
        self.cursor_info_changed.emit(line, col)
        self.line_number_area.update()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle Tab key for 4 spaces indentation, and Shift+Tab for unindent."""
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            if cursor.hasSelection():
                # Indent selected lines
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                cursor.setPosition(start)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                cursor.beginEditBlock()
                while cursor.position() < end:
                    cursor.insertText("    ")
                    end += 4
                    if not cursor.movePosition(QTextCursor.MoveOperation.Down):
                        break
                    cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
                cursor.endEditBlock()
            else:
                self.insertPlainText("    ")
            return
        elif event.key() == Qt.Key.Key_Backtab:
            # Shift+Tab unindent
            cursor = self.textCursor()
            cursor.beginEditBlock()
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            while cursor.position() <= end:
                line_text = cursor.block().text()
                spaces = len(line_text) - len(line_text.lstrip(" "))
                if spaces > 0:
                    to_remove = min(spaces, 4)
                    for _ in range(to_remove):
                        cursor.deleteChar()
                    end -= to_remove
                if not cursor.movePosition(QTextCursor.MoveOperation.Down):
                    break
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
            cursor.endEditBlock()
            return

        super().keyPressEvent(event)
