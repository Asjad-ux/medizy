"""
rx_ocr.py — Enhanced Tesseract OCR backend for prescription images
Backend only - no frontend dependencies
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image

# Update this path if Tesseract is installed in a custom location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def deskew(image):
    """Deskew image using minimum area rectangle method."""
    coords = np.column_stack(np.where(image < 255))
    if coords.size == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def preprocess_image(image_bytes):
    """Preprocess prescription image for improved Tesseract accuracy."""
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image bytes")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Scale up small images
        h, w = gray.shape
        if w < 1400:
            scale = 1400 / max(w, 1)
            gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Adaptive thresholding for uneven lighting
        thresh = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 35, 11
        )

        # Morphological cleaning
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # Sharpening
        kernel_sharp = np.array([[0, -1, 0],
                                 [-1, 5, -1],
                                 [0, -1, 0]])
        sharpened = cv2.filter2D(cleaned, -1, kernel_sharp)

        # Deskew
        deskewed = deskew(sharpened)

        return deskewed
    except Exception as e:
        raise ValueError(f"Image preprocessing failed: {str(e)}")


def get_tesseract_text(pil_img, config):
    """Run Tesseract OCR with given config and return text + confidence."""
    text = pytesseract.image_to_string(pil_img, config=config)
    data = pytesseract.image_to_data(pil_img, config=config, output_type=pytesseract.Output.DICT)

    confidences = []
    for c in data.get("conf", []):
        try:
            value = int(c)
            if value > 0:
                confidences.append(value)
        except (ValueError, TypeError):
            continue

    avg_confidence = round(sum(confidences) / len(confidences), 1) if confidences else 0.0
    return {"text": text.strip(), "confidence": avg_confidence}


def extract_text_from_prescription(image_bytes):
    """Extract text from prescription image using Tesseract."""
    try:
        processed = preprocess_image(image_bytes)
        pil_img = Image.fromarray(processed)

        configs = [
            "--oem 3 --psm 6 -l eng",   # Assume block of text
            "--oem 3 --psm 4 -l eng",   # Assume single column
            "--oem 3 --psm 7 -l eng",   # Assume single line
            "--oem 3 --psm 11 -l eng",  # Sparse text
            "--oem 3 --psm 3 -l eng"    # Fully automatic
        ]

        best = None
        for cfg in configs:
            result = get_tesseract_text(pil_img, cfg)
            if not best:
                best = result
            else:
                # Weighted scoring: confidence + text length
                score = result["confidence"] * 0.7 + len(result["text"]) * 0.3
                best_score = best["confidence"] * 0.7 + len(best["text"]) * 0.3
                if score > best_score:
                    best = result

        if not best or not best["text"]:
            return {"text": "", "confidence": 0, "success": False, "error": "Tesseract returned no text"}

        return {"text": best["text"], "confidence": best["confidence"], "success": True}
    except Exception as e:
        return {"text": "", "confidence": 0, "success": False, "error": str(e)}
