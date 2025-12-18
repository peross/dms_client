#!/usr/bin/env python3
"""Create a simple icon for the application."""
from PIL import Image, ImageDraw, ImageFont

def create_icon(output_path="icon.png", size=128):
    """Create a simple document icon."""
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw document shape (simplified - a rectangle with a folded corner)
    # Main document body
    margin = size // 8
    doc_width = size - 2 * margin
    doc_height = size - 2 * margin
    
    # Background circle
    draw.ellipse([0, 0, size-1, size-1], fill=(33, 150, 243, 255))  # Blue background
    
    # Draw document icon
    doc_margin = size // 4
    doc_x = doc_margin
    doc_y = doc_margin
    doc_w = size - 2 * doc_margin
    doc_h = size - 2 * doc_margin
    
    # Document rectangle (white)
    draw.rectangle([doc_x, doc_y, doc_x + doc_w, doc_y + doc_h], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
    
    # Folded corner effect
    corner_size = doc_w // 3
    corner_points = [
        (doc_x + doc_w - corner_size, doc_y),
        (doc_x + doc_w, doc_y),
        (doc_x + doc_w, doc_y + corner_size),
        (doc_x + doc_w - corner_size, doc_y)
    ]
    draw.polygon(corner_points, fill=(240, 240, 240, 255), outline=(200, 200, 200, 255))
    
    # Draw lines to represent text
    line_spacing = doc_h // 8
    for i in range(1, 5):
        y = doc_y + doc_h // 4 + i * line_spacing
        line_width = doc_w - 2 * (doc_w // 6) if i < 4 else doc_w // 2
        draw.rectangle([doc_x + doc_w // 6, y, doc_x + doc_w // 6 + line_width, y + 2], fill=(180, 180, 180, 255))
    
    # Save icon
    img.save(output_path, 'PNG')
    print(f"Icon created: {output_path}")

if __name__ == "__main__":
    import sys
    output_path = sys.argv[1] if len(sys.argv) > 1 else "icon.png"
    create_icon(output_path)

