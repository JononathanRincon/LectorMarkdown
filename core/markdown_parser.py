"""
Markdown to HTML conversion module for LectorMarkdown.
Produces clean, modern HTML formatted for PyQt6 QTextBrowser with zero raw markdown syntax tags.
Supports GFM tables, task lists, code syntax highlighting (Pygments), callout alerts, and themes.
"""
import re
from typing import Optional
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter

from ui.styles import get_html_css

class MarkdownParser:
    def __init__(self):
        # Configure MarkdownIt with tables and standard features
        self._current_theme = "light"
        self._md = (
            MarkdownIt("gfm-like", {
                "html": True,
                "linkify": True,
                "typographer": True,
                "highlight": self._highlight_code
            })
            .enable("table")
            .enable("strikethrough")
        )

    def _highlight_code(self, code: str, lang: str, attrs: str) -> str:
        """Syntax highlighting callback for fenced code blocks."""
        lexer = None
        clean_lang = lang.strip().lower() if lang else ""
        
        # Common aliases
        lang_map = {
            "js": "javascript",
            "ts": "typescript",
            "py": "python",
            "sh": "bash",
            "shell": "bash",
            "yml": "yaml",
            "md": "markdown",
            "ps1": "powershell"
        }
        clean_lang = lang_map.get(clean_lang, clean_lang)

        if clean_lang:
            try:
                lexer = get_lexer_by_name(clean_lang, stripall=True)
            except Exception:
                lexer = None

        if not lexer:
            try:
                # Try guessing if short, otherwise fallback
                if len(code) < 1500 and "\n" in code:
                    lexer = guess_lexer(code)
                else:
                    lexer = TextLexer()
            except Exception:
                lexer = TextLexer()

        style_name = "monokai" if self._current_theme == "dark" else "friendly"
        formatter = HtmlFormatter(
            noclasses=True,
            nowrap=True,
            style=style_name
        )
        try:
            return highlight(code, lexer, formatter)
        except Exception:
            return code

    def _preprocess_markdown(self, text: str) -> str:
        """
        Preprocess markdown to handle GitHub style alerts:
        > [!NOTE]
        > [!TIP]
        > [!IMPORTANT]
        > [!WARNING]
        > [!CAUTION]
        and enhance task lists for optimal display in QTextBrowser.
        """
        lines = text.split("\n")
        processed_lines = []
        
        alert_types = {
            "NOTE": ("ℹ️ NOTA", "callout-note"),
            "TIP": ("💡 CONSEJO", "callout-tip"),
            "IMPORTANT": ("📌 IMPORTANTE", "callout-important"),
            "WARNING": ("⚠️ ADVERTENCIA", "callout-warning"),
            "CAUTION": ("🛑 PRECAUCIÓN", "callout-caution")
        }

        i = 0
        while i < len(lines):
            line = lines[i]
            # Match alert headers like '> [!NOTE]'
            alert_match = re.match(r"^>\s*\[\!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", line, re.IGNORECASE)
            if alert_match:
                kind = alert_match.group(1).upper()
                extra_text = alert_match.group(2).strip()
                title, css_class = alert_types.get(kind, (kind, "callout-note"))
                
                # Replace with styled blockquote marker
                processed_lines.append(f'> <div class="{css_class}"><strong>{title}</strong></div>')
                if extra_text:
                    processed_lines.append(f"> {extra_text}")
                i += 1
                continue

            # Convert task list checkboxes to clean Unicode icons for QTextBrowser
            # e.g., - [x] or - [X] -> - ☑ (concluida)
            #       - [ ] -> - ☐ (pendiente)
            task_checked = re.match(r"^(\s*[-*+]\s+)\[[xX]\]\s+(.*)$", line)
            if task_checked:
                indent_bullet = task_checked.group(1)
                item_content = task_checked.group(2)
                processed_lines.append(f"{indent_bullet}<span style='color:#10b981; font-weight:bold;'>☑</span> {item_content}")
                i += 1
                continue

            task_unchecked = re.match(r"^(\s*[-*+]\s+)\[\s\]\s+(.*)$", line)
            if task_unchecked:
                indent_bullet = task_unchecked.group(1)
                item_content = task_unchecked.group(2)
                processed_lines.append(f"{indent_bullet}<span style='color:#6b7280;'>☐</span> {item_content}")
                i += 1
                continue

            processed_lines.append(line)
            i += 1

        return "\n".join(processed_lines)

    def to_html(self, markdown_text: str, theme: str = "light") -> str:
        """
        Converts markdown text to a complete, standalone styled HTML document.
        """
        if not markdown_text or not markdown_text.strip():
            # Return elegant empty state
            css = get_html_css(theme)
            return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>{css}</style></head>
<body class="{theme}">
<div class="empty-state">
    <div class="empty-icon">📖</div>
    <h2>Documento Markdown vacío</h2>
    <p>El archivo actual no tiene contenido o aún no se ha seleccionado ninguno.<br>
    Pulsa el botón de <strong>lápiz (✏️)</strong> en la barra superior para comenzar a escribir.</p>
</div>
</body>
</html>"""

        self._current_theme = theme
        preprocessed = self._preprocess_markdown(markdown_text)
        rendered_body = self._md.render(preprocessed)

        # Enhance code blocks by wrapping them in nice container divs if needed
        css = get_html_css(theme)
        
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>{css}</style>
</head>
<body class="{theme}">
<div class="markdown-container">
{rendered_body}
</div>
</body>
</html>"""
        return full_html


# Global singleton instance
parser = MarkdownParser()

def markdown_to_html(markdown_text: str, theme: str = "light") -> str:
    """Convenience helper function."""
    return parser.to_html(markdown_text, theme=theme)
