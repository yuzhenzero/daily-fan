"""Generate favicon.png from emoji using Pillow."""
import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EMOJI = '🌰'
SIZE = 64
FONT_SIZE = 52  # Slightly smaller than canvas for padding


def find_emoji_font():
    """Find an emoji-capable font on the system."""
    candidates = [
        # Windows
        'C:/Windows/Fonts/seguiemj.ttf',
        # macOS
        '/System/Library/Fonts/Apple Color Emoji.ttc',
        # Linux
        '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def generate():
    font_path = find_emoji_font()
    if font_path:
        font = ImageFont.truetype(font_path, FONT_SIZE)
    else:
        font = ImageFont.load_default()

    img = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((SIZE // 2, SIZE // 2), EMOJI, font=font,
              anchor='mm', embedded_color=True)

    output = os.path.join(SCRIPT_DIR, 'favicon.png')
    img.save(output, 'PNG')
    print(f'Generated: {output} ({SIZE}x{SIZE})')


if __name__ == '__main__':
    generate()
