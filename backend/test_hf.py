import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load env
load_dotenv()

api_key = os.getenv("HF_API_KEY")

if not api_key:
    print("❌ ERROR: HF_API_KEY not found in .env")
    exit()

# Initialize client
client = InferenceClient(api_key=api_key.strip())

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

def test_connection():
    print(f"--- 🩺 Testing with {MODEL_ID} ---")
    try:
        response = client.chat_completion(
            model=MODEL_ID,
            messages=[
                {"role": "user", "content": "Say 'Medizy is Ready' in 3 words."}
            ],
            max_tokens=20
        )

        print("✅ SUCCESS!")
        print("AI says:", response.choices[0].message.content)

    except Exception as e:
        print("❌ CONNECTION FAILED:", str(e))

if __name__ == "__main__":
    test_connection()