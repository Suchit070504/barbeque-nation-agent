def handle_booking(payload):
    # Extract info from payload
    user_id = payload.get("user_id", "unknown")

    # Build a basic response
    return {
        "response": {
            "text": f"Thank you for contacting Barbeque Nation! We'll handle your booking shortly. (User: {user_id})"
        }
    }
