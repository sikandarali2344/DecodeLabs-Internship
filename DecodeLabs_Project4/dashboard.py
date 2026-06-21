# ============================================
# PROJECT 4: COMPUTER VISION DASHBOARD WITH UPLOAD
# Batch: 2026 | DecodeLabs
# AI Engineer: Sikandar
# ============================================

from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import cv2
import numpy as np
import pytesseract
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import json
import time
from datetime import datetime
import shutil

# ============================================
# SET TESSERACT PATH (WINDOWS)
# ============================================
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.secret_key = 'decodelabs_2026_secret'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# ============================================
# FOLDERS
# ============================================
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('static', exist_ok=True)

# ============================================
# OCR FUNCTION
# ============================================

def process_ocr(image_path):
    """Process OCR on uploaded image"""
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    # Pre-processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )
    denoised = cv2.fastNlMeansDenoising(thresh)
    
    # Extract text
    start_time = time.time()
    text = pytesseract.image_to_string(denoised)
    end_time = time.time()
    
    # Get confidence data
    data = pytesseract.image_to_data(denoised, output_type=pytesseract.Output.DICT)
    
    words = []
    for i, word in enumerate(data['text']):
        if word.strip():
            confidence = int(data['conf'][i])
            if confidence > 0:
                words.append({
                    'text': word,
                    'confidence': confidence,
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i]
                })
    
    # Draw bounding boxes on image
    img_copy = image.copy()
    for w in words:
        if w['confidence'] >= 80:
            x, y, width, height = w['x'], w['y'], w['width'], w['height']
            cv2.rectangle(img_copy, (x, y), (x+width, y+height), (0, 255, 0), 2)
            cv2.putText(img_copy, f"{w['text']} ({w['confidence']}%)", 
                       (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # Save result
    result_path = 'outputs/ocr_result_upload.png'
    cv2.imwrite(result_path, img_copy)
    
    # Save text
    txt_path = 'outputs/ocr_text_upload.txt'
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("OCR EXTRACTION RESULTS\n")
        f.write(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        f.write(text)
    
    # Calculate stats
    high_conf = len([w for w in words if w['confidence'] >= 80])
    accuracy = (high_conf / len(words) * 100) if words else 0
    
    return {
        'text': text,
        'words': words,
        'total_words': len(words),
        'high_confidence': high_conf,
        'accuracy': round(accuracy, 1),
        'processing_time': round(end_time - start_time, 2),
        'image_path': result_path,
        'txt_path': txt_path
    }

# ============================================
# ROUTES
# ============================================

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and OCR processing"""
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save uploaded file
    filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    
    # Process OCR
    result = process_ocr(filepath)
    
    if result is None:
        return jsonify({'error': 'Could not process image'}), 500
    
    # Save result to session (using simple file storage)
    result['filename'] = filename
    with open('outputs/last_result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    return jsonify(result)

@app.route('/image/<filename>')
def get_image(filename):
    """Serve images"""
    try:
        return send_file(f'outputs/{filename}', mimetype='image/png')
    except:
        return "Image not found", 404

@app.route('/uploaded/<filename>')
def get_uploaded(filename):
    """Serve uploaded images"""
    try:
        return send_file(f'uploads/{filename}', mimetype='image/jpeg')
    except:
        return "Image not found", 404

@app.route('/api/result')
def get_result():
    """Get last OCR result"""
    try:
        with open('outputs/last_result.json', 'r') as f:
            return jsonify(json.load(f))
    except:
        return jsonify({'error': 'No result found'}), 404

@app.route('/about')
def about():
    return render_template('about.html')

# ============================================
# RUN
# ============================================

if __name__ == '__main__':
    print("=" * 70)
    print("📸 PROJECT 4 - OCR DASHBOARD WITH UPLOAD")
    print("=" * 70)
    print("Batch 2026 | DecodeLabs")
    print("AI Engineer: Sikandar")
    print("=" * 70)
    print("\n🚀 Dashboard running at: http://localhost:5000")
    print("📤 Upload any image to extract text!")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)