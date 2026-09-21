"""
Configuration and settings persistence for LectorMarkdown.
Uses QSettings for native Windows registry storage under HKCU\\Software\\LectorMarkdown.
"""
from typing import List
from PyQt6.QtCore import QSettings

ORG_NAME = "LectorMarkdown"
APP_NAME = "LectorMarkdown"

class Config:
    def __init__(self):
        self._settings = QSettings(ORG_NAME, APP_NAME)

    @property
    def theme(self) -> str:
        return self._settings.value("theme", "light", type=str)

    @theme.setter
    def theme(self, val: str):
        self._settings.setValue("theme", val)

    @property
    def recent_files(self) -> List[str]:
        val = self._settings.value("recent_files", [], type=list)
        return [str(f) for f in val if f]

    def add_recent_file(self, file_path: str):
        current = self.recent_files
        if file_path in current:
            current.remove(file_path)
        current.insert(0, file_path)
        # Keep last 10
        self._settings.setValue("recent_files", current[:10])

    @property
    def font_size(self) -> int:
        return self._settings.value("font_size", 14, type=int)

    @font_size.setter
    def font_size(self, val: int):
        self._settings.setValue("font_size", val)

    @property
    def window_geometry(self) -> bytes:
        return self._settings.value("window_geometry", b"")

    @window_geometry.setter
    def window_geometry(self, val: bytes):
        self._settings.setValue("window_geometry", val)

# Global singleton
config = Config()
