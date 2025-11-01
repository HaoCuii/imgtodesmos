import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import subprocess
import os
from svgpathtools import Line, CubicBezier, svg2paths
import base64
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_SIZE', 16 * 1024 * 1024))

# Configure CORS
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
if allowed_origins == '*':
    CORS(app)
else:
    CORS(app, origins=allowed_origins.split(','))

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def edge_detection(image_path, output_path):
    """Convert image to edge bitmap using OpenCV"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    inverted = cv2.bitwise_not(edges)
    cv2.imwrite(output_path, inverted)
    return output_path

def bitmap_to_svg(bitmap_path, svg_path):
    """Convert bitmap to SVG using potrace"""
    try:
        subprocess.run(['potrace', bitmap_path, '-s', '-o', svg_path], check=True)
        return svg_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Potrace conversion failed: {e}")

def svg_to_desmos(svg_path):
    """Convert SVG paths to Desmos mathematical expressions"""
    paths, attributes = svg2paths(svg_path)
    equations = []

    for i, path in enumerate(paths):
        for segment in path:
            if isinstance(segment, Line):
                x1, y1 = segment.start.real, segment.start.imag
                x2, y2 = segment.end.real, segment.end.imag
                m = (y2 - y1) / max((x2 - x1), 0.0001)
                b = y1 - m * x1
                slope_threshold = 1

                if abs(m) <= slope_threshold:
                    domain_min = min(x1, x2)
                    domain_max = max(x1, x2)
                    equation = f'y = {m}x + {b} \\left\\{{ {domain_min:.2f} \\leq x \\leq {domain_max:.2f} \\right\\}}'
                    equations.append(equation)
                else:
                    if m == float('inf'):
                        equation = f'x = {x1:.2f} \\left\\{{ {min(y1, y2):.2f} \\leq y \\leq {max(y1, y2):.2f} \\right\\}}'
                        equations.append(equation)

            elif isinstance(segment, CubicBezier):
                x0, y0 = segment.start.real, segment.start.imag
                x1, y1 = segment.control1.real, segment.control1.imag
                x2, y2 = segment.control2.real, segment.control2.imag
                x3, y3 = segment.end.real, segment.end.imag

                x_expr = (
                    f"(1 - t)^3*{x0:.1f} + "
                    f"3*t*(1 - t)^2*{x1:.1f} + "
                    f"3*t^2*(1 - t)*{x2:.1f} + "
                    f"t^3*{x3:.1f}"
                )
                y_expr = (
                    f"(1 - t)^3*{y0:.1f} + "
                    f"3*t*(1 - t)^2*{y1:.1f} + "
                    f"3*t^2*(1 - t)*{y2:.1f} + "
                    f"t^3*{y3:.1f}"
                )

                equation = f'\\left({x_expr},{y_expr}\\right)'
                equations.append(equation)

    return equations

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """Process uploaded image and return Desmos equations"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)

        # Process image
        edges_path = os.path.join(OUTPUT_FOLDER, 'edges.bmp')
        svg_path = os.path.join(OUTPUT_FOLDER, 'output.svg')

        # Edge detection
        edge_detection(image_path, edges_path)

        # Convert to SVG
        bitmap_to_svg(edges_path, svg_path)

        # Generate Desmos equations
        equations = svg_to_desmos(svg_path)

        # Read edge image as base64
        with open(edges_path, 'rb') as f:
            edges_base64 = base64.b64encode(f.read()).decode('utf-8')

        return jsonify({
            'success': True,
            'equations': equations,
            'edgesImage': f'data:image/bmp;base64,{edges_base64}',
            'equationCount': len(equations)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
