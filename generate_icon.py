"""
Script to generate a professional multi-resolution application icon (icon.ico)
for Lector Markdown on Windows.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_app_icon(output_path="assets/icon.ico"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # We will generate a master 512x512 image and downscale to various icon sizes
    size = 512
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background rounded rectangle (squircle) with gradient
    margin = 24
    rect_box = [margin, margin, size - margin, size - margin]
    radius = 100
    
    # Create gradient background
    gradient = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gradient)
    
    # Draw vertical linear gradient from #3b82f6 (blue) to #6366f1 (indigo) to #8b5cf6 (violet)
    for y in range(margin, size - margin):
        ratio = (y - margin) / (size - 2 * margin)
        # RGB interpolation
        r = int(37 + ratio * (124 - 37))
        g = int(99 + ratio * (58 - 99))
        b = int(235 + ratio * (237 - 235))
        g_draw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255))
        
    # Mask with rounded rectangle
    mask = Image.new("L", (size, size), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle(rect_box, radius=radius, fill=255)
    
    img.paste(gradient, (0, 0), mask)
    
    # Subtle inner border/glow
    draw.rounded_rectangle(rect_box, radius=radius, outline=(255, 255, 255, 60), width=6)
    
    # Draw Markdown symbol:
    # Stylized "M" and downward arrow "↓"
    # Left side: M
    # Right side: Arrow
    white = (255, 255, 255, 245)
    
    # Draw stylized 'M'
    # Coordinates for 'M'
    m_left = 90
    m_top = 160
    m_w = 170
    m_h = 190
    stroke = 34
    
    # M points:
    # Left column: (m_left, m_top) to (m_left, m_top + m_h)
    draw.line([(m_left, m_top), (m_left, m_top + m_h)], fill=white, width=stroke)
    # Left diagonal: (m_left, m_top) to (m_left + m_w/2, m_top + m_h * 0.75)
    draw.line([(m_left, m_top), (m_left + m_w//2, int(m_top + m_h * 0.75))], fill=white, width=stroke)
    # Right diagonal: (m_left + m_w/2, m_top + m_h * 0.75) to (m_left + m_w, m_top)
    draw.line([(m_left + m_w//2, int(m_top + m_h * 0.75)), (m_left + m_w, m_top)], fill=white, width=stroke)
    # Right column: (m_left + m_w, m_top) to (m_left + m_w, m_top + m_h)
    draw.line([(m_left + m_w, m_top), (m_left + m_w, m_top + m_h)], fill=white, width=stroke)
    
    # Draw Arrow "↓"
    a_x = 360
    a_top = 160
    a_h = 190
    # Shaft
    draw.line([(a_x, a_top), (a_x, a_top + a_h - 20)], fill=white, width=stroke)
    # Arrowhead
    head_w = 60
    head_y = a_top + a_h - 10
    draw.line([(a_x - head_w, head_y - 65), (a_x, head_y)], fill=white, width=stroke)
    draw.line([(a_x + head_w, head_y - 65), (a_x, head_y)], fill=white, width=stroke)
    
    # Draw bottom accent line / dot
    draw.rounded_rectangle([90, 390, 420, 404], radius=6, fill=(255, 255, 255, 180))
    
    # Save as PNG
    png_path = "assets/icon.png"
    img.save(png_path, format="PNG")
    
    # Save as multi-resolution ICO
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(output_path, format="ICO", sizes=sizes)
    print(f"Icon created successfully at {output_path} and {png_path}")

if __name__ == "__main__":
    create_app_icon()
