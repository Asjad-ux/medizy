import os
import re
import logging
from huggingface_hub import InferenceClient
from database import (
    check_medicine_stock,
    find_closest_medicine,
    get_cheapest_option,
    get_nearest_store,
    get_alternatives,
    get_online_prices
)
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(api_key=os.getenv("HF_API_KEY").strip())

MEDICAL_KEYWORDS = {
    "medicine", "drug", "tablet", "capsule", "injection", "prescription", "pharmacy",
    "dose", "dosage", "tablet", "pill", "prescribe", "symptom", "symptoms", "treatment",
    "treat", "infection", "health", "illness", "disease", "doctor", "clinic", "hospital",
    "allergy", "fever", "cough", "cold", "headache", "pain", "blood pressure", "diabetes",
    "cholesterol", "asthma", "covid", "virus", "bacteria", "side effect", "side-effects",
    "vaccination", "vaccine", "antibiotic", "antacid", "stomach", "headache", "dental",
    "joint", "arthritis", "skin", "antidepressant", "antihistamine", "medicine name"
}

NON_MEDICAL_PATTERNS = [
    r"prime minister", r"president", r"who is", r"what is", r"where is", r"when is",
    r"who was", r"election", r"government", r"politics", r"sport", r"movie", r"music",
    r"actor", r"actress", r"singer", r"weather", r"capital", r"country", r"history"
]

# 🔍 Extract medicine
def extract_medicine_name(text):
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    return " ".join(words)


def is_medical_query(text):
    text_lower = text.lower()
    words = set(re.findall(r'\b[a-zA-Z0-9]+\b', text_lower))
    if words & MEDICAL_KEYWORDS:
        return True

    medicine_guess = find_closest_medicine(extract_medicine_name(text))
    if medicine_guess:
        return True

    for pattern in NON_MEDICAL_PATTERNS:
        if re.search(pattern, text_lower):
            return False
    return False


def get_medibot_response(user_message, history=None):
    if history is None:
        history = []
    response = None
    try:
        msg_lower = user_message.lower()

        if not is_medical_query(user_message):
            response = (
                "⚠️ I only answer medical, health, pharmacy, or prescription-related questions. "
                "Please ask about medicines, symptoms, treatments, availability, or doctor/pharmacy guidance."
            )
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response})
            return response, history

        # 🧠 Context memory (dynamic)
        last_med = None
        for msg in reversed(history):
            if msg["role"] == "assistant":
                last_med = extract_medicine_name(msg["content"])
                break

        if "that medicine" in msg_lower or "you mentioned" in msg_lower:
            if last_med:
                user_message += f" ({last_med})"

        # ⚠️ Safety
        if any(phrase in msg_lower for phrase in ["can i take", "dosage", "side effects", "mix with alcohol"]):
            return (
                "⚠️ Please consult a doctor before taking any medicine. "
                "I can provide general info, but dosage and safety depend on your condition."
            ), history

        # 🔍 Detect medicine
        med_name = extract_medicine_name(user_message)
        med_name = find_closest_medicine(med_name)

        if med_name:
            results = check_medicine_stock(med_name)
            if results:
                cheapest = get_cheapest_option(results)
                nearest = get_nearest_store(results)
                alternatives = get_alternatives(med_name)
                online_prices = get_online_prices(med_name)

                response = f"""
💊 {med_name} Availability:

🔹 Cheapest: {cheapest['store_name']} - ₹{cheapest['price']} (Stock: {cheapest['quantity']})
📍 Nearest: {nearest['store_name']} ({round(nearest['distance'],2)} km away)
🔄 Alternatives: {", ".join(alternatives)}

📦 All options:
"""
                for r in results[:5]:
                    response += f"\n- {r['store_name']} → ₹{r['price']} (Stock: {r['quantity']})"

                if online_prices:
                    response += "\n\n🌐 Online Prices:\n"
                    response += f"PharmEasy: ₹{online_prices['PharmEasy']}, NetMeds: ₹{online_prices['NetMeds']}, TATA1mg: ₹{online_prices['TATA1mg']}, DawaIndia: ₹{online_prices['DawaIndia']}"

                history.append({"role": "user", "content": user_message})
                history.append({"role": "assistant", "content": response})
                return response, history

        # 🤖 AI fallback
        messages = [
            {"role": "system", "content": "You are Medibot. Only answer medical or website queries. Stay short."}
        ] + history + [
            {"role": "user", "content": user_message}
        ]

        completion = client.chat_completion(model=MODEL_ID, messages=messages, max_tokens=200)

        if completion and completion.choices:
            response = completion.choices[0].message.content
        else:
            response = "⚠️ No response generated."

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})

        return response, history

    except Exception as e:
        logging.error("ERROR: %s", e)
        return "⚠️ Something went wrong.", history


def get_prescription_bot_message(results):
    try:
        if not results:
            return "I could not identify any medicines from the prescription right now."

        summary_lines = []
        for item in results:
            if item.get("in_stock"):
                summary_lines.append(
                    f"{item['medicine']} is available at {item.get('cheapest_store', 'a nearby pharmacy')} for ₹{item.get('cheapest_price', 'N/A')}"
                )
            else:
                summary_lines.append(f"{item['medicine']} is currently not in stock.")

        prompt = (
            "You are Medibot. The user has uploaded a prescription and you have the detected medicines "
            "with availability information. Respond with a short popup message that says which medicines were detected, "
            "provides a brief use case or purpose for each medicine, and confirms the pharmacy stock status. "
            "Use a friendly, clear tone."
        )

        user_text = "Detected prescription medicines and availability:\n" + "\n".join(summary_lines)

        messages = [
            {"role": "system", "content": "You are Medibot. Keep the response short, friendly, and precise."},
            {"role": "user", "content": prompt + "\n\n" + user_text}
        ]

        completion = client.chat_completion(model=MODEL_ID, messages=messages, max_tokens=200)

        if completion and completion.choices:
            return completion.choices[0].message.content.strip()

        return "⚠️ I could not generate a bot summary at this time."

    except Exception as e:
        logging.error("Bot summary error: %s", e)
        return "⚠️ Unable to generate a bot summary right now."
