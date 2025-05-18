import json
import os
import uuid
from utils.logger import log_conversation

# Load state prompts
PROMPTS_DIR = 'state_machine/prompts'
prompts = {}
for filename in os.listdir(PROMPTS_DIR):
    if filename.endswith('.json'):
        with open(os.path.join(PROMPTS_DIR, filename)) as f:
            prompt_data = json.load(f)
            prompts[prompt_data['state']] = prompt_data

# Load transitions
with open('state_machine/transitions.json') as f:
    transitions = json.load(f)

# Track user session data
user_id = str(uuid.uuid4())
visited_states = []
booking_status = "Not Confirmed"
unanswered_questions = []

# Simulated intent extraction (can be improved later)
def extract_intent(user_input):
    if "book" in user_input.lower():
        return "make_booking"
    elif any(word in user_input.lower() for word in ["bangalore", "delhi", "location"]):
        return "provide_city"
    elif any(char.isdigit() for char in user_input) and len(user_input) >= 10:
        return "provide_contact"
    elif any(word in user_input.lower() for word in ["pm", "am", "date", "time"]):
        return "provide_date_time"
    elif "cancel" in user_input.lower():
        return "cancel_booking"
    elif "update" in user_input.lower():
        return "update_booking"
    elif "faq" in user_input.lower() or "question" in user_input.lower():
        return "ask_faq"
    else:
        return "unknown"

# State transition function
def get_next_state(current_state, intent):
    for transition in transitions:
        if transition['current_state'] == current_state and transition['intent'] == intent:
            return transition['next_state']
    return None

# Main engine loop
current_state = "Greeting"
while current_state:
    visited_states.append(current_state)
    prompt = prompts.get(current_state)
    print(prompt['instruction'])
    user_input = input("You: ")
    intent = extract_intent(user_input)
    next_state = get_next_state(current_state, intent)

    if not next_state:
        print("Sorry, I didn't understand that. Could you please rephrase?")
        unanswered_questions.append(user_input)
        continue

    if next_state == "Confirm_Booking":
        booking_status = "Confirmed"
        print("Thank you! Your booking has been confirmed.")
        break

    current_state = next_state

# After conversation ends, log the session
log_conversation(user_id, visited_states, booking_status, len(unanswered_questions))
