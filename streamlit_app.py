import streamlit as st
import json
import os
from state_machine_engine import extract_intent, get_next_state, prompts, transitions

st.set_page_config(page_title="Barbeque Nation Chatbot")
st.title("🤖 Barbeque Nation Chatbot")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_state" not in st.session_state:
    st.session_state.current_state = "Greeting"
if "visited_states" not in st.session_state:
    st.session_state.visited_states = []

# Display system prompt
if st.session_state.current_state:
    prompt = prompts.get(st.session_state.current_state, {}).get("instruction", "")
    st.chat_message("assistant").write(prompt)

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.visited_states.append(st.session_state.current_state)

    intent = extract_intent(user_input)
    next_state = get_next_state(st.session_state.current_state, intent)

    if not next_state:
        st.session_state.messages.append((user_input, "Sorry, I didn't understand."))
        st.chat_message("assistant").write("Sorry, I didn't understand. Can you rephrase?")
    else:
        st.session_state.current_state = next_state
        next_prompt = prompts.get(next_state, {}).get("instruction", "")
        st.chat_message("assistant").write(next_prompt)
