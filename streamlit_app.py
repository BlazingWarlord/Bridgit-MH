import streamlit as st
import time
import os
import google.generativeai as genai

# Function for bot response
def bot_reply(user_message):
    genai.configure(api_key='AIzaSyBDBFgNWh6U2QGX9I4kiZWnZt7iXseKJeg')

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="You are Bridgit, a mental health specialist aimed to help people between ages 10-100 with their mental health issues. You must help out the patient until they say they are satisfied with the session",
    )

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(user_message)

    return f"Bridgit: {response.text}"

# Initialize the user's credits if not already set
if "credits" not in st.session_state:
    st.session_state["credits"] = 100

# Custom CSS for fixed input box and color scheme
st.markdown(
    """
    <style>
    /* Main page styling */
    body {
        background-color: white;
        color: black;
    }
    /* Chat bubbles */
    .user-message {
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        border: 2px white
    }
    .bot-message {
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        border: 2px white
    }
    /* Fix input form to the bottom */
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #e9f5ea;
        padding: 10px;
        box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title and sub-header with green accent
st.markdown("<h1>Meet Bridgit</h1>", unsafe_allow_html=True)
st.markdown("<h3>Your Mental Health Companion</h3>", unsafe_allow_html=True)

# Sidebar content, showing credits
st.sidebar.markdown("**Credits:**")
st.sidebar.markdown(f"{st.session_state['credits']}")

# Chat area (main content)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display the messages as bubbles
for message in st.session_state["messages"]:
    if message.startswith("You:"):
        st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)  # Light green for user
    else:
        st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)  # Light red for bot

# Text input and send button, fixed to the bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", key="user_input")
    submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        # Deduct 1 credit when user sends a message
        if st.session_state["credits"] > 0:
            st.session_state["credits"] -= 1
            # Add user message
            st.session_state["messages"].append(f"You: {user_input}")
        else:
            st.warning("You don't have enough credits!")

# If user message was just sent, add bot reply after a delay
if len(st.session_state["messages"]) > 0 and st.session_state["messages"][-1].startswith("You:"):
    # Wait for 10 seconds before showing bot message
    time.sleep(10)
    bot_response = bot_reply(st.session_state["messages"][-1][5:])  # Extract user message without "You: "
    st.session_state["messages"].append(f"Bot: {bot_response}")

# Fixed input box
st.markdown("<div class='fixed-bottom'><form action='#'></form></div>", unsafe_allow_html=True)
