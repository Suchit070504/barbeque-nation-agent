from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import hmac
import hashlib
from booking_handler import handle_booking

load_dotenv()

app = Flask(__name__)
RETELL_SECRET = os.getenv("RETELL_SECRET")

def verify_signature(request):
    signature = request.headers.get("retell-signature")
    if not signature:
        return False
    body = request.get_data()
    expected_signature = hmac.new(RETELL_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@app.route("/retell-callback", methods=["POST"])
def retell_callback():
    if not verify_signature(request):
        return jsonify({"error": "Invalid signature"}), 403

    payload = request.json
    response = handle_booking(payload)  # You will implement this logic
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)
