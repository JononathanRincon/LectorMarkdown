"""
Theme styling and stylesheets for LectorMarkdown.
Contains HTML/CSS for the rendered document and QSS for the PyQt6 UI.
"""

def get_html_css(theme: str = "light") -> str:
    """Returns CSS styles embedded inside the HTML document for QTextBrowser."""
    if theme == "dark":
        bg_color = "#1e1e2e"
        text_color = "#cdd6f4"
        heading_color = "#89b4fa"
        h2_border = "#313244"
        link_color = "#89b4fa"
        inline_code_bg = "#313244"
        inline_code_color = "#f38ba8"
        code_block_bg = "#181825"
        code_block_border = "#313244"
        blockquote_bg = "#181825"
        blockquote_border = "#89b4fa"
        table_border = "#313244"
        table_th_bg = "#181825"
        table_zebra_bg = "#222235"
        hr_color = "#313244"
        empty_sub = "#a6adc8"
    else:
        bg_color = "#ffffff"
        text_color = "#1e293b"
        heading_color = "#0f172a"
        h2_border = "#e2e8f0"
        link_color = "#2563eb"
        inline_code_bg = "#f1f5f9"
        inline_code_color = "#e11d48"
        code_block_bg = "#f8fafc"
        code_block_border = "#e2e8f0"
        blockquote_bg = "#f8fafc"
        blockquote_border = "#3b82f6"
        table_border = "#e2e8f0"
        table_th_bg = "#f1f5f9"
        table_zebra_bg = "#f8fafc"
        hr_color = "#e2e8f0"
        empty_sub = "#64748b"

    return f"""
    body {{
        background-color: {bg_color};
        color: {text_color};
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
        font-size: 15px;
        line-height: 1.7;
        margin: 0;
        padding: 24px 36px;
    }}
    .markdown-container {{
        max-width: 880px;
        margin: 0 auto;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {heading_color};
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 600;
        margin-top: 28px;
        margin-bottom: 12px;
        line-height: 1.3;
    }}
    h1 {{
        font-size: 26px;
        padding-bottom: 8px;
        border-bottom: 2px solid {h2_border};
        margin-top: 10px;
    }}
    h2 {{
        font-size: 21px;
        padding-bottom: 6px;
        border-bottom: 1px solid {h2_border};
    }}
    h3 {{ font-size: 18px; }}
    h4 {{ font-size: 16px; }}
    h5 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}
    h6 {{ font-size: 13px; color: {empty_sub}; }}

    p {{
        margin-top: 0;
        margin-bottom: 16px;
    }}
    strong, b {{
        font-weight: 700;
    }}
    em, i {{
        font-style: italic;
    }}
    s, strike, del {{
        text-decoration: line-through;
        opacity: 0.75;
    }}
    a {{
        color: {link_color};
        text-decoration: none;
    }}
    blockquote {{
        margin: 16px 0;
        padding: 10px 18px;
        background-color: {blockquote_bg};
        border-left: 4px solid {blockquote_border};
        border-radius: 4px;
    }}
    code {{
        font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
        font-size: 13.5px;
        background-color: {inline_code_bg};
        color: {inline_code_color};
        padding: 2px 5px;
        border-radius: 4px;
    }}
    pre {{
        background-color: {code_block_bg};
        border: 1px solid {code_block_border};
        border-radius: 6px;
        padding: 14px 18px;
        margin: 16px 0;
        font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
        font-size: 13.5px;
        line-height: 1.5;
        overflow-x: auto;
    }}
    pre code {{
        background-color: transparent;
        color: inherit;
        padding: 0;
        border-radius: 0;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }}
    th, td {{
        border: 1px solid {table_border};
        padding: 10px 14px;
        text-align: left;
    }}
    th {{
        background-color: {table_th_bg};
        font-weight: 600;
    }}
    tr:nth-child(even) {{
        background-color: {table_zebra_bg};
    }}
    ul, ol {{
        margin-top: 0;
        margin-bottom: 16px;
        padding-left: 26px;
    }}
    li {{
        margin-bottom: 6px;
    }}
    hr {{
        border: 0;
        height: 1px;
        background-color: {hr_color};
        margin: 26px 0;
    }}
    img {{
        max-width: 100%;
        border-radius: 6px;
        margin: 12px 0;
    }}
    .callout-note {{ color: #3b82f6; }}
    .callout-tip {{ color: #10b981; }}
    .callout-important {{ color: #a855f7; }}
    .callout-warning {{ color: #f59e0b; }}
    .callout-caution {{ color: #ef4444; }}

    .empty-state {{
        text-align: center;
        padding: 60px 20px;
        color: {empty_sub};
    }}
    .empty-icon {{
        font-size: 54px;
        margin-bottom: 16px;
    }}
    .empty-state h2 {{
        color: {heading_color};
        margin-bottom: 8px;
        border: none;
    }}
    """

def get_app_qss(theme: str = "light") -> str:
    """Returns the QSS stylesheet for the PyQt6 application."""
    if theme == "dark":
        return """
        QMainWindow {
            background-color: #181825;
        }
        QToolBar {
            background-color: #1e1e2e;
            border-bottom: 1px solid #313244;
            padding: 5px 8px;
            spacing: 6px;
        }
        QToolButton {
            background-color: transparent;
            color: #cdd6f4;
            border: 1px solid transparent;
            border-radius: 5px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 500;
        }
        QToolButton:hover {
            background-color: #313244;
            border-color: #45475a;
        }
        QToolButton:pressed {
            background-color: #45475a;
        }
        QToolButton:checked {
            background-color: #313244;
            border-color: #89b4fa;
            color: #89b4fa;
        }
        QToolBar::separator {
            width: 1px;
            background-color: #313244;
            margin: 4px 6px;
        }
        QStatusBar {
            background-color: #1e1e2e;
            color: #a6adc8;
            border-top: 1px solid #313244;
            font-size: 12px;
        }
        QStatusBar QLabel {
            color: #a6adc8;
            padding: 2px 8px;
        }
        QPlainTextEdit {
            background-color: #181825;
            color: #cdd6f4;
            border: none;
            selection-background-color: #45475a;
            selection-color: #cdd6f4;
            font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            padding: 16px 20px;
        }
        QTextBrowser {
            background-color: #1e1e2e;
            border: none;
            selection-background-color: #45475a;
            selection-color: #cdd6f4;
        }
        QScrollBar:vertical {
            background-color: #181825;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #313244;
            min-height: 25px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #45475a;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background-color: #181825;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background-color: #313244;
            min-width: 25px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #45475a;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        /* Search Bar */
        QFrame#searchFrame {
            background-color: #1e1e2e;
            border-bottom: 1px solid #313244;
            padding: 6px 12px;
        }
        QLineEdit#searchInput {
            background-color: #181825;
            color: #cdd6f4;
            border: 1px solid #313244;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 13px;
        }
        QLineEdit#searchInput:focus {
            border-color: #89b4fa;
        }
        QPushButton#searchButton {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #45475a;
            border-radius: 5px;
            padding: 5px 12px;
            font-size: 12px;
        }
        QPushButton#searchButton:hover {
            background-color: #45475a;
        }
        """
    else:
        return """
        QMainWindow {
            background-color: #f8fafc;
        }
        QToolBar {
            background-color: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            padding: 5px 8px;
            spacing: 6px;
        }
        QToolButton {
            background-color: transparent;
            color: #334155;
            border: 1px solid transparent;
            border-radius: 5px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 500;
        }
        QToolButton:hover {
            background-color: #f1f5f9;
            border-color: #cbd5e1;
        }
        QToolButton:pressed {
            background-color: #e2e8f0;
        }
        QToolButton:checked {
            background-color: #eff6ff;
            border-color: #3b82f6;
            color: #1d4ed8;
        }
        QToolBar::separator {
            width: 1px;
            background-color: #e2e8f0;
            margin: 4px 6px;
        }
        QStatusBar {
            background-color: #ffffff;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
            font-size: 12px;
        }
        QStatusBar QLabel {
            color: #64748b;
            padding: 2px 8px;
        }
        QPlainTextEdit {
            background-color: #ffffff;
            color: #1e293b;
            border: none;
            selection-background-color: #bfdbfe;
            selection-color: #1e3a8a;
            font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            padding: 16px 20px;
        }
        QTextBrowser {
            background-color: #ffffff;
            border: none;
            selection-background-color: #bfdbfe;
            selection-color: #1e3a8a;
        }
        QScrollBar:vertical {
            background-color: #f8fafc;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #cbd5e1;
            min-height: 25px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #94a3b8;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background-color: #f8fafc;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background-color: #cbd5e1;
            min-width: 25px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #94a3b8;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        /* Search Bar */
        QFrame#searchFrame {
            background-color: #ffffff;
            border-bottom: 1px solid #e2e8f0;
            padding: 6px 12px;
        }
        QLineEdit#searchInput {
            background-color: #f8fafc;
            color: #0f172a;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 13px;
        }
        QLineEdit#searchInput:focus {
            border-color: #2563eb;
            background-color: #ffffff;
        }
        QPushButton#searchButton {
            background-color: #f1f5f9;
            color: #334155;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 5px 12px;
            font-size: 12px;
        }
        QPushButton#searchButton:hover {
            background-color: #e2e8f0;
        }
        """
