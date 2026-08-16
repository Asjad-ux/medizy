import mysql.connector
import os
from dotenv import load_dotenv
from rapidfuzz import process
import math

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

# Fuzzy match
def find_closest_medicine(user_input):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT medicine_name FROM medicines")
    meds = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    match, score, _ = process.extractOne(user_input, meds)
    return match if score and score > 60 else None

# Stock + price
def check_medicine_stock(med_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT m.medicine_name, m.price, m.quantity, s.name AS store_name,
           s.latitude, s.longitude
    FROM medicines m
    JOIN medical_stores s ON m.store_id = s.id
    WHERE m.medicine_name LIKE %s
    """

    cursor.execute(query, (f"%{med_name}%",))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# Cheapest
def get_cheapest_option(results):
    return min(results, key=lambda x: x['price'])

# Distance (Haversine)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Nearest pharmacy
def get_nearest_store(results, user_lat=28.52, user_lon=77.25):
    for r in results:
        r['distance'] = calculate_distance(user_lat, user_lon, r['latitude'], r['longitude'])
    return min(results, key=lambda x: x['distance'])

# Alternatives
def get_alternatives(med_name):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT DISTINCT medicine_name FROM medicines
    WHERE medicine_name != %s
    LIMIT 5
    """
    cursor.execute(query, (med_name,))
    results = [r[0] for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results

# Online price comparison
def get_online_prices(med_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM online_prices_wide WHERE medicine_name = %s"
    cursor.execute(query, (med_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Get all medicine names for AI matching
def get_all_medicine_names():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Hum sirf unique names nikal rahe hain taaki AI confusion na ho
        query = "SELECT DISTINCT medicine_name FROM medicines"
        cursor.execute(query)
        
        # Converting all names into a list
        results = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Database Error in get_all_medicine_names: {e}")
        return []
