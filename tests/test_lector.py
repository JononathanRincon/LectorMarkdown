"""
Automated unit tests for LectorMarkdown.
Verifies markdown parsing, file operations, state management, and UI logic.
"""
import os
import sys
import tempfile
import unittest

from PyQt6.QtWidgets import QApplication

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.markdown_parser import MarkdownParser, markdown_to_html
from core.file_manager import FileManager
from core.windows_registry import get_executable_command
from ui.main_window import MainWindow

# Initialize headless QApplication for testing Qt widgets
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.parser = MarkdownParser()

    def test_headings_and_formatting(self):
        md = "# Título Principal\n\nTexto en **negrita** y en *cursiva* y ~~tachado~~."
        html = self.parser.to_html(md, theme="light")
        self.assertIn("<h1>Título Principal</h1>", html)
        self.assertIn("<strong>negrita</strong>", html)
        self.assertIn("<em>cursiva</em>", html)
        self.assertIn("<s>tachado</s>", html)

    def test_tables(self):
        md = "| Encabezado 1 | Encabezado 2 |\n|---|---|\n| Dato A | Dato B |"
        html = self.parser.to_html(md, theme="light")
        self.assertIn("<table>", html)
        self.assertIn("<th>Encabezado 1</th>", html)
        self.assertIn("<td>Dato A</td>", html)

    def test_task_lists(self):
        md = "- [x] Tarea completa\n- [ ] Tarea pendiente"
        html = self.parser.to_html(md, theme="light")
        self.assertIn("☑", html)
        self.assertIn("☐", html)
        self.assertIn("Tarea completa", html)
        self.assertIn("Tarea pendiente", html)

    def test_code_highlighting(self):
        md = "```python\ndef calcular(x):\n    return x * 2\n```"
        html = self.parser.to_html(md, theme="light")
        self.assertIn("<pre>", html)
        # Should contain highlighted span from Pygments
        self.assertIn("calcular", html)
        self.assertIn("def", html)

    def test_alerts_callouts(self):
        md = "> [!NOTE]\n> Esta es una nota informativa."
        html = self.parser.to_html(md, theme="light")
        self.assertIn("callout-note", html)
        self.assertIn("NOTA", html)

    def test_empty_content(self):
        html = self.parser.to_html("", theme="light")
        self.assertIn("Documento Markdown vacío", html)

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.fm = FileManager()

    def test_load_sample_file(self):
        sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample.md"))
        ok, content, enc = self.fm.load_file(sample_path)
        self.assertTrue(ok)
        self.assertIn("Documento de Prueba", content)
        self.assertEqual(self.fm.filename, "sample.md")
        self.assertFalse(self.fm.is_modified)

    def test_save_and_reload(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tf:
            temp_path = tf.name

        try:
            test_content = "# Test Guardado\n\nContenido con acentos: áéíóú ñ y emojis: 🚀✨"
            ok, msg = self.fm.save_file(test_content, temp_path)
            self.assertTrue(ok)

            # Reload and verify UTF-8 integrity
            ok2, reloaded_content, enc = self.fm.load_file(temp_path)
            self.assertTrue(ok2)
            self.assertEqual(reloaded_content, test_content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_stats(self):
        text = "Una dos tres cuatro cinco seis siete ocho nueve diez."
        stats = self.fm.get_stats(text)
        self.assertEqual(stats["words"], 10)
        self.assertEqual(stats["reading_minutes"], 1)

class TestWindowsRegistry(unittest.TestCase):
    def test_executable_command_format(self):
        command, icon_path = get_executable_command()
        self.assertIn("%1", command)
        self.assertTrue(os.path.exists(icon_path))

    def test_registry_registration(self):
        from core.windows_registry import (
            register_windows_integration,
            is_context_menu_registered,
            is_file_association_registered
        )
        ok, msg = register_windows_integration()
        self.assertTrue(ok)
        self.assertTrue(is_context_menu_registered())
        self.assertTrue(is_file_association_registered())

class TestMainWindow(unittest.TestCase):
    def test_window_flow(self):
        sample_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample.md"))
        window = MainWindow(initial_file=sample_path)
        
        # Initial mode should be Reading Mode (index 0)
        self.assertEqual(window.stack.currentIndex(), 0)
        self.assertIn("Modo Lectura", window.status_mode.text())
        self.assertTrue(window.action_edit.isVisible())
        self.assertFalse(window.action_save.isVisible())

        # Switch to Editor Mode
        window.switch_to_editor_mode()
        self.assertEqual(window.stack.currentIndex(), 1)
        self.assertIn("Modo Edición", window.status_mode.text())
        self.assertFalse(window.action_edit.isVisible())
        self.assertTrue(window.action_save.isVisible())

        # Simulate editing text
        window.editor_view.setPlainText("# Contenido Editado\n\nNueva línea")
        self.assertTrue(window.file_manager.is_modified)

        # Switch theme
        window.toggle_theme()
        self.assertEqual(window.current_theme, "dark")
        window.toggle_theme()
        self.assertEqual(window.current_theme, "light")

if __name__ == "__main__":
    unittest.main()
