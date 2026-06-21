# create_samples.py
import cv2
import numpy as np
import os

os.makedirs('images', exist_ok=True)

# ============================================
# CREATE TEXT IMAGE FOR OCR
# ============================================
img = np.ones((400, 800, 3), dtype=np.uint8) * 255
texts = [
    ("DecodeLabs AI", (50, 80), 60),
    ("Project 4: Computer Vision", (50, 160), 40),
    ("OCR - Optical Character Recognition", (50, 240), 35),
    ("Batch 2026 | Sikandar", (50, 320), 28),
]
for text, pos, size in texts:
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, size/30, (0,0,0), 2)

cv2.imwrite('images/sample_text.png', img)
print("✅ Created: images/sample_text.png")

# ============================================
# CREATE OBJECT IMAGE FOR DETECTION
# ============================================
img2 = np.ones((600, 800, 3), dtype=np.uint8) * 220

# Person
cv2.rectangle(img2, (100, 150), (200, 400), (0, 0, 255), -1)
cv2.circle(img2, (150, 120), 30, (0, 0, 255), -1)

# Car
cv2.rectangle(img2, (500, 300), (700, 420), (0, 255, 0), -1)

# Dog
cv2.ellipse(img2, (120, 400), (40, 30), 0, 0, 360, (139, 69, 19), -1)
cv2.ellipse(img2, (90, 380), (20, 15), 0, 0, 360, (139, 69, 19), -1)
cv2.ellipse(img2, (150, 380), (20, 15), 0, 0, 360, (139, 69, 19), -1)

cv2.putText(img2, "DecodeLabs - Object Detection", (200, 50), 
           cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

cv2.imwrite('images/sample_objects.jpg', img2)
print("✅ Created: images/sample_objects.jpg")

print("\n✅ All sample images created!")