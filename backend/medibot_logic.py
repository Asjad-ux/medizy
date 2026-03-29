import os
import re
from huggingface_hub import InferenceClient
from database import (
    check_medicine_stock,
    find_closest_medicine,
    get_cheapest_option,
    get_nearest_store,
    get_alternatives
)
from dotenv import load_dotenv

load_dotenv()

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(api_key=os.getenv("HF_API_KEY").strip())


# 🔍 Extract text
def extract_medicine_name(text):
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    return " ".join(words)


# 🧠 Get last medicine from history
def get_last_medicine(history):
    for msg in reversed(history):
        if msg["role"] == "assistant":
            text = msg["content"].lower()
            for med in ["paracetamol", "aspirin", "crocin", "ibuprofen"]:
                if med in text:
                    return med
    return None


def get_medibot_response(user_message, history=[]):
    try:
        msg_lower = user_message.lower()

        # 🧠 CONTEXT MEMORY
        last_med = get_last_medicine(history)

        if any(word in msg_lower for word in ["it", "its", "that medicine"]):
            if last_med:
                user_message += f" ({last_med})"

        # ❌ NON-MEDICAL FILTER
        non_medical_keywords = [
            "prime minister", "football", "cricket", "movie",
            "chatgpt", "ai", "google", "best player"
        ]

        if any(word in msg_lower for word in non_medical_keywords):
            response = "⚠️ I only handle medical and pharmacy-related queries."

            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response})

            return response, history

        # ⚠️ SAFETY
        if "can i take" in msg_lower:
            response = (
                "⚠️ Please consult a doctor before taking any medicine. "
                "For mild headaches, Paracetamol is commonly used."
            )

            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response})

            return response, history

        # 🔍 MEDICINE DETECTION
        med_name = extract_medicine_name(user_message)
        med_name = find_closest_medicine(med_name)

        if med_name:
            results = check_medicine_stock(med_name)

            if results:
                cheapest = get_cheapest_option(results)
                nearest = get_nearest_store(results)
                alternatives = get_alternatives(med_name)

                # 🧠 INTENT DETECTION
                if "price" in msg_lower:
                    response = f"💰 Price of {med_name}: ₹{cheapest['price']} (at {cheapest['store_name']})"

                elif "cheapest" in msg_lower:
                    response = f"💰 Cheapest {med_name}: {cheapest['store_name']} - ₹{cheapest['price']}"

                elif "nearest" in msg_lower or "near" in msg_lower:
                    response = f"📍 Nearest {med_name}: {nearest['store_name']} ({round(nearest['distance'],2)} km away)"

                elif "alternative" in msg_lower:
                    response = f"🔄 Alternatives for {med_name}: {', '.join(alternatives)}"

                else:
                    # FULL RESPONSE (default)
                    response = f"""
💊 {med_name} Availability:

🔹 Cheapest: {cheapest['store_name']} - ₹{cheapest['price']} (Stock: {cheapest['quantity']})

📍 Nearest: {nearest['store_name']} ({round(nearest['distance'],2)} km away)

🔄 Alternatives: {", ".join(alternatives)}

📦 All options:
"""

            for r in results[:5]:
                response += f"\n- {r['store_name']} → ₹{r['price']} (Stock: {r['quantity']})"

        # ✅ SAVE HISTORY
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})

        return response, history

        # 🤖 AI FALLBACK
        messages = [
            {
                "role": "system",
                "content": "You are Medibot. Only answer medical or pharmacy queries. Keep answers short."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        completion = client.chat_completion(
            model=MODEL_ID,
            messages=messages,
            max_tokens=200
        )

        response = completion.choices[0].message.content

        # ✅ SAVE HISTORY
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})

        return response, history

    except Exception as e:
        print("ERROR:", e)
        return "⚠️ Something went wrong.", history