"""
app.py — Medizy Flask Backend
Main application with Chatbot + Prescription features
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from medibot_logic import get_medibot_response, get_prescription_bot_message
from dotenv import load_dotenv
import logging
import os
import werkzeug

from rx_ocr import extract_text_from_prescription
from rx_handler import (
    get_medicines_from_db,
    extract_medicine_candidates,
    match_medicines,
    build_results
)

load_dotenv()

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
CORS(app)

logging.basicConfig(level=logging.INFO)

# Session storage
sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    """Medibot chat endpoint"""
    try:
        data = request.json
        user_msg = data.get("message", "")
        user_id = data.get("user_id", "default")
        
        history = sessions.get(user_id, [])
        reply, updated_history = get_medibot_response(user_msg, history)
        sessions[user_id] = updated_history
        
        return jsonify({"status": "success", "reply": reply})
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ──────────────────── PRESCRIPTION UPLOAD ENDPOINT ────────────────────────
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UPLOAD_FOLDER = "backend/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload-prescription', methods=['POST'])
def upload_prescription():
    """
    Prescription upload and analysis endpoint
    
    Flow:
    1. Receive image file
    2. Run Tesseract OCR
    3. Extract medicine candidates
    4. Match against database
    5. Query for pricing and availability
    6. Return structured results
    """
    
    print("\n" + "="*80)
    print("[API] POST /upload-prescription received")
    print("="*80)
    
    try:
        # Step 1: Validate file
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file provided"
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"File type not allowed. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "success": False,
                "error": f"File too large. Max size: 10 MB"
            }), 413
        
        print(f"[API] File received: {file.filename} ({file_size} bytes)")
        
        # Step 2: Read image bytes
        image_bytes = file.read()
        
        # Step 3: Run OCR
        print("[API] Running Tesseract OCR...")
        ocr_result = extract_text_from_prescription(image_bytes)
        
        if not ocr_result['success']:
            print(f"[API] OCR failed: {ocr_result.get('error', 'Unknown error')}")
            return jsonify({
                "success": False,
                "error": f"OCR failed: {ocr_result.get('error', 'Could not extract text')}"
            }), 422
        
        extracted_text = ocr_result['text'].strip()
        confidence = ocr_result['confidence']
        
        if not extracted_text:
            print("[API] No text extracted from image")
            return jsonify({
                "success": False,
                "error": "No text could be extracted. Please upload a clearer image.",
                "medicines_found": [],
                "results": []
            }), 422
        
        print(f"[API] OCR successful - {len(extracted_text)} chars, confidence: {confidence}%")
        
        # Step 4: Get database medicines
        print("[API] Fetching medicines from database...")
        db_medicines = get_medicines_from_db()
        
        if not db_medicines:
            print("[API] ERROR: No medicines in database")
            return jsonify({
                "success": False,
                "error": "Could not load medicine database"
            }), 500
        
        print(f"[API] Found {len(db_medicines)} medicines in database")
        
        # Step 5: Extract and match medicines
        print("[API] Extracting medicine candidates...")
        candidates = extract_medicine_candidates(extracted_text)
        print(f"[API] Found {len(candidates)} candidates")
        
        print("[API] Matching medicines...")
        matched = match_medicines(candidates, db_medicines, threshold=70)
        medicine_names = [m['name'] for m in matched]
        print(f"[API] Matched {len(medicine_names)} medicines")
        
        # Step 6: Get location (optional)
        user_lat = request.form.get('user_lat', type=float)
        user_lon = request.form.get('user_lon', type=float)
        
        # Step 7: Build results
        print("[API] Building pharmacy results...")
        results = build_results(medicine_names, user_lat, user_lon)
        print(f"[API] Built {len(results)} result entries")
        
        print("[API] Generating Medibot summary...")
        bot_message = get_prescription_bot_message(results)
        print("[API] Bot message generated")
        
        # Step 8: Return response
        response = {
            "success": True,
            "extracted_text": extracted_text,
            "ocr_confidence": confidence,
            "medicines_found": medicine_names,
            "match_details": matched,
            "results": results,
            "bot_message": bot_message
        }
        
        if not medicine_names:
            response["warning"] = (
                "No medicines from our database were detected. "
                "Try uploading a clearer image."
            )
        
        print("[API] SUCCESS - Returning response")
        print("="*80 + "\n")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"[API] EXCEPTION: {e}")
        print("="*80 + "\n")
        logging.error(f"Prescription upload error: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

# Health Check Point

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Starting Medizy Flask Server")
    print("="*80)
    print("• Chatbot endpoint:      POST /chat")
    print("• Prescription endpoint: POST /upload-prescription")
    print("• Health check:          GET /health")
    print("="*80 + "\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')
