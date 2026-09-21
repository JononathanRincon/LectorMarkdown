"""
Icon and graphical resources generator for LectorMarkdown.
Generates crisp, high-DPI resolution QIcon objects dynamically.
"""
from typing import Tuple
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QFont
from PyQt6.QtCore import Qt, QPointF, QRectF

def _create_canvas(size: int = 32) -> Tuple[QPixmap, QPainter]:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    return pixmap, painter

def get_pencil_icon(color_hex: str = "#3b82f6") -> QIcon:
    """Generates a modern pencil (edit) icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(color))

    # Pencil body rotated 45 degrees
    p.save()
    p.translate(24, 24)
    p.rotate(45)

    # Pencil body
    path = QPainterPath()
    path.addRoundedRect(QRectF(-6, -16, 12, 24), 2, 2)
    p.fillPath(path, QBrush(color))

    # Pencil tip
    tip_path = QPainterPath()
    tip_path.moveTo(-6, 8)
    tip_path.lineTo(6, 8)
    tip_path.lineTo(0, 16)
    tip_path.closeSubpath()
    p.fillPath(tip_path, QBrush(color))

    # Eraser top
    eraser_path = QPainterPath()
    eraser_path.addRoundedRect(QRectF(-6, -20, 12, 4), 1, 1)
    p.fillPath(eraser_path, QBrush(color.lighter(130)))

    p.restore()
    p.end()
    return QIcon(pixmap)

def get_save_icon(color_hex: str = "#10b981") -> QIcon:
    """Generates a modern floppy disk (save) icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    
    # Outer disk body
    path = QPainterPath()
    path.moveTo(8, 8)
    path.lineTo(34, 8)
    path.lineTo(40, 14)
    path.lineTo(40, 40)
    path.lineTo(8, 40)
    path.closeSubpath()
    p.fillPath(path, QBrush(color))

    # Inner shutter (top label)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(QColor(255, 255, 255, 220)))
    p.drawRoundedRect(QRectF(14, 8, 20, 14), 2, 2)

    # Shutter metal chip
    p.setBrush(QBrush(color.darker(120)))
    p.drawRoundedRect(QRectF(18, 10, 6, 8), 1, 1)

    # Bottom label
    p.setBrush(QBrush(QColor(255, 255, 255, 230)))
    p.drawRoundedRect(QRectF(13, 26, 22, 14), 2, 2)

    p.end()
    return QIcon(pixmap)

def get_reader_icon(color_hex: str = "#6366f1") -> QIcon:
    """Generates a modern reading / eye icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    
    pen = QPen(color, 4)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    # Eye outline
    path = QPainterPath()
    path.moveTo(6, 24)
    path.quadTo(24, 10, 42, 24)
    path.quadTo(24, 38, 6, 24)
    p.drawPath(path)

    # Pupil
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(color))
    p.drawEllipse(QRectF(18, 18, 12, 12))

    p.setBrush(QBrush(QColor(255, 255, 255)))
    p.drawEllipse(QRectF(22, 20, 4, 4))

    p.end()
    return QIcon(pixmap)

def get_folder_icon(color_hex: str = "#f59e0b") -> QIcon:
    """Generates an open folder icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(color.darker(115)))

    # Back folder flap
    path = QPainterPath()
    path.moveTo(6, 12)
    path.lineTo(18, 12)
    path.lineTo(22, 16)
    path.lineTo(42, 16)
    path.lineTo(42, 38)
    path.lineTo(6, 38)
    path.closeSubpath()
    p.fillPath(path, QBrush(color.darker(115)))

    # Front folder flap
    p.setBrush(QBrush(color))
    front = QPainterPath()
    front.moveTo(4, 20)
    front.lineTo(44, 20)
    front.lineTo(40, 40)
    front.lineTo(8, 40)
    front.closeSubpath()
    p.fillPath(front, QBrush(color))

    p.end()
    return QIcon(pixmap)

def get_sun_icon(color_hex: str = "#f59e0b") -> QIcon:
    """Generates a sun icon for Light mode."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    p.setPen(QPen(color, 3.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    p.setBrush(QBrush(color))

    # Center circle
    p.drawEllipse(QRectF(16, 16, 16, 16))

    # Rays
    rays = [
        (24, 6, 24, 11),
        (24, 37, 24, 42),
        (6, 24, 11, 24),
        (37, 24, 42, 24),
        (11, 11, 15, 15),
        (33, 33, 37, 37),
        (11, 37, 15, 33),
        (33, 15, 37, 11)
    ]
    for x1, y1, x2, y2 in rays:
        p.drawLine(x1, y1, x2, y2)

    p.end()
    return QIcon(pixmap)

def get_moon_icon(color_hex: str = "#818cf8") -> QIcon:
    """Generates a crescent moon icon for Dark mode."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(color))

    # Outer circle
    path1 = QPainterPath()
    path1.addEllipse(QRectF(10, 8, 28, 28))

    # Inner cut circle
    path2 = QPainterPath()
    path2.addEllipse(QRectF(16, 6, 26, 26))

    moon = path1.subtracted(path2)
    p.fillPath(moon, QBrush(color))

    p.end()
    return QIcon(pixmap)

def get_search_icon(color_hex: str = "#64748b") -> QIcon:
    """Generates a magnifying glass search icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    pen = QPen(color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    # Circle
    p.drawEllipse(QRectF(10, 10, 20, 20))
    # Handle
    p.drawLine(25, 25, 38, 38)

    p.end()
    return QIcon(pixmap)

def get_zoom_in_icon(color_hex: str = "#64748b") -> QIcon:
    """Generates a zoom in icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    pen = QPen(color, 3.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    p.drawEllipse(QRectF(8, 8, 22, 22))
    p.drawLine(24, 24, 38, 38)
    # Plus sign
    p.drawLine(19, 14, 19, 24)
    p.drawLine(14, 19, 24, 19)

    p.end()
    return QIcon(pixmap)

def get_zoom_out_icon(color_hex: str = "#64748b") -> QIcon:
    """Generates a zoom out icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    pen = QPen(color, 3.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)

    p.drawEllipse(QRectF(8, 8, 22, 22))
    p.drawLine(24, 24, 38, 38)
    # Minus sign
    p.drawLine(14, 19, 24, 19)

    p.end()
    return QIcon(pixmap)

def get_windows_icon(color_hex: str = "#0078d4") -> QIcon:
    """Generates a Windows integration icon."""
    pixmap, p = _create_canvas(48)
    color = QColor(color_hex)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(color))

    # Four square tiles of Windows logo
    s = 13
    gap = 4
    x0, y0 = 9, 9
    p.drawRoundedRect(QRectF(x0, y0, s, s), 1.5, 1.5)
    p.drawRoundedRect(QRectF(x0 + s + gap, y0, s, s), 1.5, 1.5)
    p.drawRoundedRect(QRectF(x0, y0 + s + gap, s, s), 1.5, 1.5)
    p.drawRoundedRect(QRectF(x0 + s + gap, y0 + s + gap, s, s), 1.5, 1.5)

    p.end()
    return QIcon(pixmap)
