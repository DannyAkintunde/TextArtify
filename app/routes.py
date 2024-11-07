from flask import Blueprint, jsonify, send_file, request
import logging
import hashlib
import io
import os
from app import cache
from app import utils

bp = Blueprint('main', __name__)
v1 = Blueprint('v1', __name__)

@bp.route('/')
def docs():
    return 'Check our github for docs'

# version 1 routes

fonts = utils.load_fonts_from_dir()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@v1.route('/text-to-image', methods=['GET', 'POST'])
@cache.cached(timeout=60, query_string=True)  # Cache results for 60 seconds
def text_to_image():
    data = request.get_json() if request.method == 'POST' else {}
    
    text = request.args.get('text') or data.get('text')
    font = request.args.get('font') or data.get('font')
    font_size = request.args.get('font_size') or data.get('font_size') or 52
    text_color = request.args.get('color') or data.get('color') or '#FFFFFFFF'
    bg_color = request.args.get('bg_color') or data.get('bg_color') or '#000000FF'
    min_size = int(request.args.get('min_size') or data.get('min_size') or 0)
    max_size = int(request.args.get('max_size') or data.get('max_size') or 0)
    text_align = request.args.get('text_align') or data.get('text_align')
    padding_ratio = float(request.args.get('padding_ratio') or data.get('padding_ratio') or 0.1)
    
    if not text:
        logger.error("Text is required")
        return jsonify({"error": "Text is required"}), 400
    
    if isinstance(text_align, str) and text_align.lower() not in ('center', 'left', 'right'):
        logger.error("Invalid text alignment specified")
        return jsonify({"error": "Invalid text_align value make sure you specify one of the following center, right, left."}), 400
    
    font_path = utils.get_font(fonts, font)
    if not font_path:
        logger.warning("Font not found, using default font")

    # Create a unique cache key based on input parameters
    # cache_key = hashlib.md5(f"{text}{font}{font_size}{text_color}{bg_color}{min_size}{max_size}".encode()).hexdigest()

    # Check if the image is cached
    """
    cached_image = cache.get(cache_key)
    if cached_image:
        logger.info("Returning cached image")
        return send_file(io.BytesIO(cached_image), mimetype='image/png')
    """
    
    try:
        img = utils.create_image_with_text(
            text,
            utils.hex_to_rgba(text_color),
            utils.hex_to_rgba(bg_color),
            font_path,
            int(font_size),
            min_size=min_size,
            max_size=max_size,
            padding_ratio=padding_ratio,
            alignment=text_align
        )

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)  # Move to the beginning of the BytesIO buffer

        logger.info("Image created successfully")

        # cache.set(cache_key, img_bytes.getvalue(), timeout=60)  # Cache for 60 seconds

        return send_file(img_bytes, mimetype='image/png')

    except Exception as e:
        logger.error(f"Error creating image: {e}")
        return jsonify({"error": "Failed to create image"}), 500

@v1.route('/add-text-to-img', methods=['GET', 'POST'])
def add_text_to_image():
    data = request.get_json() if request.method == 'POST' else {}
    
    text = request.args.get('text') or data.get('text')
    bg = request.args.get('bg') or data.get('bg')
    font = request.args.get('font') or data.get('font')
    font_size = request.args.get('font_size') or data.get('font_size') or 52
    text_color = request.args.get('color') or data.get('color') or '#FFFFFFFF'
    text_align = request.args.get('text_align') or data.get('text_align')
    padding_ratio = float(request.args.get('padding_ratio') or data.get('padding_ratio') or 0.1)

    if not text:
        logger.error("Text is required")
        return jsonify({"error": "Text is required"}), 400
    
    if not bg:
        logger.error("bg is required")
        return jsonify({"error": "bg is required"}), 400
    elif not utils.is_valid_url(bg):
        logger.error("Invalid url recived")
        return jsonify({"error": "Invalid url"}), 400
    
    if isinstance(text_align, str) and text_align.lower() not in ('center', 'left', 'right'):
        logger.error("Invalid text alignment specified")
        return jsonify({"error": "Invalid text_align value make sure you specify one of the following center, right, left."}), 400
    
    font_path = utils.get_font(fonts, font)
    if not font_path:
        logger.warning("Font not found, using default font")
    
    try:
        bg_image = utils.save_file_from_url(bg)
        
        if bg_image:
            img = utils.add_text_to_image(
              bg_image,
              text,
              font_path,
              int(font_size),
              utils.hex_to_rgba(text_color),
              padding_ratio,
              text_align
            )
              
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)  # Move to the beginning of the BytesIO buffer

            logger.info("Image created successfully")
              
            return send_file(img_bytes, mimetype='image/png')
        else:
            return jsonify({"error": "Invalid image"}), 400
    except Exception as e:
        logger.error(f"Error creating image: {e}")
        return jsonify({"error": "Failed to create image"}), 500


i = 0  

@bp.route('/test-img')
def test():
    global i
    ext = request.args.get('ext') 
    exts = ('png', 'jpg')

    if ext and ext not in exts:
        return 'error', 400 

    if not ext:
        i += 1 
        if i > 2:
            i = 0
        ext = exts[i - 1]

    return send_file(f"../static/test.{ext}")