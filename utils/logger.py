import csv
import os

def log_conversation(user_id, states, booking_status, unanswered_questions):
    file_path = 'data/conversation_logs.csv'

    # Create file and header if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["User ID", "States Visited", "Booking Status", "Unanswered Questions"])

    # Append the conversation log
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, " -> ".join(states), booking_status, unanswered_questions])
