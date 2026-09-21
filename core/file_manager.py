"""
File manager module for LectorMarkdown.
Handles safe file loading, encoding detection, atomic saving, and state tracking.
"""
import os
import time
from typing import Optional, Tuple

class FileManager:
    def __init__(self):
        self.file_path: Optional[str] = None
        self.original_content: str = ""
        self.current_content: str = ""
        self.is_modified: bool = False
        self.encoding_used: str = "utf-8"
        self.last_saved_mtime: float = 0.0

    @property
    def has_file(self) -> bool:
        return bool(self.file_path and os.path.exists(self.file_path))

    @property
    def filename(self) -> str:
        if self.file_path:
            return os.path.basename(self.file_path)
        return "Sin título.md"

    @property
    def directory(self) -> str:
        if self.file_path:
            return os.path.dirname(os.path.abspath(self.file_path))
        return os.path.expanduser("~")

    def load_file(self, path: str) -> Tuple[bool, str, str]:
        """
        Loads a markdown file from disk.
        Returns (success: bool, content_or_error: str, encoding: str).
        """
        if not os.path.exists(path):
            return False, f"El archivo no existe: {path}", ""

        abs_path = os.path.abspath(path)
        encodings_to_try = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
        content = ""
        used_encoding = "utf-8"

        for enc in encodings_to_try:
            try:
                with open(abs_path, "r", encoding=enc) as f:
                    content = f.read()
                used_encoding = enc
                break
            except (UnicodeDecodeError, LookupError):
                continue
        else:
            return False, f"No se pudo decodificar el archivo {path} con codificaciones estándar.", ""

        self.file_path = abs_path
        self.original_content = content
        self.current_content = content
        self.is_modified = False
        self.encoding_used = used_encoding
        try:
            self.last_saved_mtime = os.path.getmtime(abs_path)
        except OSError:
            self.last_saved_mtime = time.time()

        return True, content, used_encoding

    def save_file(self, content: str, target_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Saves content to target_path or self.file_path using UTF-8 encoding.
        Returns (success: bool, message: str).
        """
        path_to_save = target_path or self.file_path
        if not path_to_save:
            return False, "No se ha especificado ninguna ruta para guardar."

        abs_path = os.path.abspath(path_to_save)
        
        try:
            # Ensure parent directory exists
            parent_dir = os.path.dirname(abs_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            # Write file in UTF-8
            with open(abs_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

            self.file_path = abs_path
            self.original_content = content
            self.current_content = content
            self.is_modified = False
            self.encoding_used = "utf-8"
            self.last_saved_mtime = os.path.getmtime(abs_path)
            return True, f"Guardado correctamente en {os.path.basename(abs_path)}"
        except Exception as e:
            return False, f"Error al guardar el archivo: {str(e)}"

    def set_modified(self, modified: bool, current_content: str = ""):
        self.is_modified = modified
        if current_content:
            self.current_content = current_content

    def check_external_modification(self) -> bool:
        """Returns True if the file on disk was modified externally since last load/save."""
        if not self.has_file:
            return False
        try:
            current_mtime = os.path.getmtime(self.file_path)
            return current_mtime > (self.last_saved_mtime + 1.0)
        except OSError:
            return False

    def get_stats(self, content: Optional[str] = None) -> dict:
        """Calculates words, characters, and estimated reading time."""
        text = content if content is not None else self.current_content
        char_count = len(text)
        words = text.split()
        word_count = len(words)
        # Average reading speed: 200 words/min
        reading_minutes = max(1, round(word_count / 200)) if word_count > 0 else 0
        return {
            "characters": char_count,
            "words": word_count,
            "reading_minutes": reading_minutes
        }
