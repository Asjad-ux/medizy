from flask import Flask, request, jsonify
from flask_cors import CORS
from medibot_logic import get_medibot_response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    user_id = data.get("user_id", "default")

    history = sessions.get(user_id, [])

    reply, updated_history = get_medibot_response(user_msg, history)
    sessions[user_id] = updated_history

    return jsonify({"status": "success", "reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)