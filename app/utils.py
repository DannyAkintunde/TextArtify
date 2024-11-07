from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import re
import requests
import tempfile
from urllib.parse import urlparse
from . import config

def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

def hex_to_rgba(hex_code):
    hex_code = hex_code.lstrip('#')
    
    if len(hex_code) not in (6, 8):
        raise ValueError("Invalis hex code, hex code must be 6 to 9 characters long.")
    
    # Extract the red, green, and blue components
    r = int(hex_code[0:2], 16)  # Convert the first two characters to decimal
    g = int(hex_code[2:4], 16)  # Convert the next two characters to decimal
    b = int(hex_code[4:6], 16)  # Convert the last two characters to decimal
    
    if len(hex_code) == 8:
        a = int(hex_code[6:8], 16)
        return (r, g, b, a)
    
    return (r, g, b, 255)

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the max width
        test_line = f"{current_line} {word}".strip()
        bbox = font.getbbox(test_line)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)  # Add the last line
    return lines


def get_image_suffix(content_type):
    """Map MIME types to file extensions."""
    mime_to_extension = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/bmp': '.bmp',
        'image/webp': '.webp',
        'image/tiff': '.tiff'
    }
    return mime_to_extension.get(content_type)

def save_file_from_url(url):
    """
    Save a temporary file from url and returns the file path
    Returns: string file path to temp file
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            extension = get_image_suffix(content_type)
            
            if not extension:
                print("Unsupported content type: {}".format(content_type))
                return
            
            # Create a temporary file with the correct extension
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as file:
                file.write(response.content)
                filename = file.name  # Get the name of the temporary file
                print(f"File saved as: {filename}")
                return filename
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred: {}".format(err))
        raise err
    except Exception as e:
        print("An error occurred: {}".format(e))
        raise e


# fonts
def load_fonts_from_dir():
    """Loads font from the fonts directory"""
    directory_path = Path('static/fonts').resolve()
    files = [file for file in directory_path.iterdir() if file.is_file()]
    return files

def get_font(fonts, font):
    """
    Get font from font path list
    Returns: Path
    """
    fonts = list(filter(lambda f: f.stem == font, fonts))
    
    if len(fonts) > 0:
        return fonts[0]
    
    return fonts

def create_image_with_text(text, color, bg_color, font_path=None, font_size=150, min_size=None, max_size=None, padding_ratio=0.1, alignment='center'):
    """Generate an image with wrapped text."""
    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default(font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return None

    # Calculate padding based on the image size
    def calculate_padding(size):
        return int(size * padding_ratio)

    # Start with a default image size calculation
    min_size = min_size or 300
    inputed_max_size = max_size
    max_size = max_size or min_size * 2
    
    # Create a temporary image to calculate text dimensions
    temp_img = Image.new('RGBA', (max_size, max_size), color=bg_color)
    temp_draw = ImageDraw.Draw(temp_img)

    # Wrap the text to fit within the specified width
    available_width = max_size - 2 * calculate_padding(max_size)
    wrapped_lines = wrap_text(text, font, available_width)

    # Calculate the longest line width
    longest_line_width = max(font.getbbox(line)[2] - font.getbbox(line)[0] for line in wrapped_lines)
    
    # Calculate line height and total text height
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1]  # Height of a single line
    total_text_height = (line_height + line_height // 2) * len(wrapped_lines)

    # Determine the final image size based on content
    final_width = max(longest_line_width + 2 * calculate_padding(min_size), min_size)
    final_height = max(total_text_height + 2 * calculate_padding(min_size), min_size)

    # Ensure final size does not exceed max_size
    final_size = min(max(final_width, final_height), max_size) if inputed_max_size else max(final_width, final_height)

    # Re-calculate available width for the final image size
    available_width = final_size - 2 * calculate_padding(final_size)
    
    # Re-wrap the text using the final available width
    wrapped_lines = wrap_text(text, font, available_width)

    # Create the final image
    img = Image.new('RGBA', (final_size, final_size), color=bg_color)
    text_image = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(text_image)

    # Calculate the starting y-coordinate to center the text vertically
    total_text_height = (line_height + line_height // 2) * len(wrapped_lines)
    y_text = (final_size - total_text_height) / 2

    # Add text to the image
    for line in wrapped_lines:
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        
        if alignment == 'left':
            x_text = 0 + calculate_padding(final_size)  # Left aligned
        elif alignment == 'right':
            x_text = final_size - line_width - calculate_padding(final_size)  # Right aligned
        else:  # center
            x_text = (final_size - line_width) / 2  # Centered
        
        d.text((x_text, y_text), line, font=font, fill=color)
        y_text += line_height + line_height // 2  # Move down for the next line

    return Image.alpha_composite(img, text_image)

def add_text_to_image(image_file, text, font_path, font_size, color, padding_ratio=0.1, alignment='center'):
    """Overlay text on an image."""
    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default(font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return None

    def calculate_padding(size):
        return int(size * padding_ratio)

    image = Image.open(image_file).convert('RGBA')
    image_width, image_height = image.size
    available_width = image_width - 2 * calculate_padding(image_width)
    
    wrapped_lines = wrap_text(text, font, available_width)

    line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
    total_text_height = (line_height + line_height // 2) * len(wrapped_lines)

    text_image = Image.new('RGBA', image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(text_image)

    y_text = (image_height - total_text_height) / 2

    for line in wrapped_lines:
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]

        if alignment == 'left':
            x_text = calculate_padding(image_width)  # Left aligned
        elif alignment == 'right':
            x_text = image_width - line_width - calculate_padding(image_width)  # Right aligned
        else:  # center
            x_text = (image_width - line_width) / 2  # Centered

        # Draw the text on the text image
        d.text((x_text, y_text), line, font=font, fill=color)
        y_text += line_height + line_height // 2

    return Image.alpha_composite(image, text_image)

# Example usage:
if __name__ == "__main__":
    img = create_image_with_text(
        text="Hello, World! This is a dynamically generated image with wrapped text.",
        color="black",
        bg_color="white",
        font_path="arial.ttf",  # Change to your font path
        font_size=40,
        min_size=300,
        max_size=800,
        padding_ratio=0.1
    )
    if img:
        img.show()  # Display the image