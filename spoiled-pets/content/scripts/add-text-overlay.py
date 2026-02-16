#!/usr/bin/env python3
"""
Add text overlay to slideshow images for TikTok.
Usage: python3 add-text-overlay.py <input_image> <output_image> <text> [--position top|center|bottom] [--style hook|content|cta]

Styles:
  hook    — Large bold text, slight tilt effect, max impact (slide 1)
  content — Clean medium text, easy to read (slides 2-5)
  cta     — Bold with accent color (final slide)
"""

import sys
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont


def find_font(bold=True):
    """Find a TikTok-style font on macOS. Futura Bold = closest to TikTok 'Classic'."""
    # Priority order: Futura Bold > Avenir Heavy > Avenir Black > fallbacks
    preferred = [
        ("/System/Library/Fonts/Supplemental/Futura.ttc", 2),   # Futura Bold
        ("/System/Library/Fonts/Avenir.ttc", 4),                 # Avenir Heavy
        ("/System/Library/Fonts/Avenir.ttc", 2),                 # Avenir Black
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
    ]
    for path, index in preferred:
        if os.path.exists(path):
            return (path, index)
    return None


def add_text_overlay(input_path, output_path, text, position="center", style="content"):
    img = Image.open(input_path).convert("RGBA")
    
    # Create overlay for semi-transparent background
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    w, h = img.size
    
    # Font sizing based on style (tuned for Futura Bold / TikTok-style fonts)
    if style == "hook":
        font_size = int(h * 0.065)  # Big and bold
        max_chars_per_line = 16
    elif style == "cta":
        font_size = int(h * 0.052)
        max_chars_per_line = 20
    else:  # content
        font_size = int(h * 0.050)
        max_chars_per_line = 22
    
    font_info = find_font(bold=True)
    if font_info:
        font_path, font_index = font_info
        font = ImageFont.truetype(font_path, font_size, index=font_index)
    else:
        font = ImageFont.load_default()
    
    # Wrap text
    lines = textwrap.wrap(text, width=max_chars_per_line)
    
    # Calculate text block size
    line_spacing = int(font_size * 1.3)
    text_block_height = len(lines) * line_spacing
    
    # Position the text block
    padding = int(h * 0.04)
    if position == "top":
        y_start = int(h * 0.12)
    elif position == "bottom":
        y_start = h - text_block_height - int(h * 0.18)
    else:  # center
        y_start = (h - text_block_height) // 2
    
    # Draw text with outline for readability (no background box — TikTok native style)
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (w - line_width) // 2
        y = y_start + i * line_spacing
        
        # Text outline (thicker stroke for readability without background)
        outline_width = max(3, font_size // 15)
        draw.text((x, y), line, font=font, fill="white",
                  stroke_width=outline_width, stroke_fill="black")
    
    # Composite overlay onto original
    result = Image.alpha_composite(img, overlay)
    
    # Convert back to RGB for JPEG output
    if output_path.lower().endswith(('.jpg', '.jpeg')):
        result = result.convert("RGB")
    
    result.save(output_path, quality=92)
    print(f"Saved: {output_path} ({w}x{h}, style={style}, pos={position})")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Add text overlay to slideshow images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("text", help="Text to overlay")
    parser.add_argument("--position", choices=["top", "center", "bottom"], default="center")
    parser.add_argument("--style", choices=["hook", "content", "cta"], default="content")
    args = parser.parse_args()
    
    add_text_overlay(args.input, args.output, args.text, args.position, args.style)
