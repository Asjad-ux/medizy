"""
rx_handler.py — Extract medicines from OCR text and lookup in database
"""

import re
from rapidfuzz import fuzz, process
from database import get_connection
import math

# Medicine name patterns
DOSE_PATTERN = re.compile(
    r'\b(\d+\s?(?:mg|mcg|ml|g|iu|units?|tab|cap|syrup|drops?))\b',
    re.IGNORECASE
)

STOPWORDS = {
    "the", "and", "with", "for", "take", "once", "twice", "daily", "morning",
    "evening", "night", "before", "after", "food", "meals", "day", "days",
    "tablet", "tablets", "capsule", "capsules", "syrup", "drops", "use", "as",
    "directed", "rx", "dr", "doctor", "patient", "name", "age", "date", "address"
}


def get_medicines_from_db():
    """Fetch all medicine names from database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT medicine_name FROM medicines")
        medicines = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return medicines
    except Exception as e:
        print(f"ERROR fetching medicines from DB: {e}")
        return []


def extract_medicine_candidates(text):
    """Extract potential medicine names from OCR text"""
    candidates = set()
    lines = text.split('\n')
    
    def add_ngrams(words):
        for i in range(len(words)):
            candidates.add(words[i].lower())
        for i in range(len(words) - 1):
            candidates.add(f"{words[i]} {words[i+1]}".lower())
        for i in range(len(words) - 2):
            candidates.add(f"{words[i]} {words[i+1]} {words[i+2]}".lower())

    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        name_part = DOSE_PATTERN.sub('', line).strip()
        name_part = re.sub(r'[^a-zA-Z\s\-]', ' ', name_part).strip()
        words = name_part.split()
        filtered = [w for w in words if len(w) >= 3 and w.lower() not in STOPWORDS]
        
        if not filtered:
            continue
        
        add_ngrams(filtered)
        if len(filtered) <= 5:
            candidates.add(' '.join(filtered).lower())
    
    return list(candidates)


def match_medicines(candidates, db_medicines, threshold=65):
    """Fuzzy match candidates against database medicines"""
    if not db_medicines:
        return []
    
    db_lower = {m.lower(): m for m in db_medicines}
    db_keys = list(db_lower.keys())
    matched = {}
    
    for candidate in candidates:
        results = process.extract(
            candidate,
            db_keys,
            scorer=fuzz.token_set_ratio,
            limit=3
        )
        
        for match_key, score, _ in results:
            if score >= threshold:
                original_name = db_lower[match_key]
                if original_name not in matched or matched[original_name]['score'] < score:
                    matched[original_name] = {
                        'name': original_name,
                        'score': score
                    }
    
    return sorted(matched.values(), key=lambda x: x['score'], reverse=True)


def get_medicine_availability(medicine_name):
    """Get all stores with this medicine in stock"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                m.medicine_name,
                m.price,
                m.quantity,
                ms.name AS store_name,
                ms.latitude,
                ms.longitude,
                m.store_id
            FROM medicines m
            JOIN medical_stores ms ON m.store_id = ms.id
            WHERE LOWER(m.medicine_name) LIKE LOWER(%s)
              AND m.quantity > 0
            ORDER BY m.price ASC
        """
        
        cursor.execute(query, (f"%{medicine_name}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results
        
    except Exception as e:
        print(f"ERROR getting medicine availability: {e}")
        return []


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates (Haversine)"""
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return round(R * c, 2)


def build_results(medicine_names, user_lat=None, user_lon=None):
    """Build final results with cheapest and nearest stores"""
    results = []
    
    for med_name in medicine_names:
        availability = get_medicine_availability(med_name)
        
        result = {
            "medicine": med_name,
            "in_stock": len(availability) > 0,
            "cheapest_store": None,
            "cheapest_price": None,
            "nearest_store": None,
            "nearest_distance": None,
            "all_stores": []
        }
        
        if availability:
            # Find cheapest
            cheapest = min(availability, key=lambda x: float(x['price']))
            result["cheapest_store"] = cheapest['store_name']
            result["cheapest_price"] = float(cheapest['price'])
            
            # Find nearest (if location provided)
            if user_lat and user_lon:
                for store in availability:
                    dist = calculate_distance(
                        user_lat, user_lon,
                        float(store['latitude']), float(store['longitude'])
                    )
                    store['_distance'] = dist
                
                nearest = min(availability, key=lambda x: x['_distance'])
                result["nearest_store"] = nearest['store_name']
                result["nearest_distance"] = nearest['_distance']
            
            # All stores
            result["all_stores"] = [
                {
                    "store_name": s['store_name'],
                    "price": float(s['price']),
                    "quantity": s['quantity'],
                    "distance": s.get('_distance', None)
                }
                for s in availability
            ]
        
        results.append(result)
    
    return results
