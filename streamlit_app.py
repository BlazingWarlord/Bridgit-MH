import streamlit as st
import time
import os
import google.generativeai as genai

# Hardcoded users for demonstration (you can replace with a database or external authentication system)
USER_CREDENTIALS = {"user1": "password123", "user2": "pass456"}

# Initialize login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Function to check login credentials
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password")

# Login form if not logged in
if not st.session_state.logged_in:
    st.title("Login to Meet Bridgit")
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            login(username, password)

# If logged in, show the chat app
if st.session_state.logged_in:
    st.title("Meet Bridgit")
    st.header(f"Your AI Mental Health Companion, {st.session_state.username}")

    # Initialize history in session state
    if "hist" not in st.session_state:
        st.session_state.hist = []

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
            system_instruction="You are Bridgit, a mental health specialist...",
        )

        chat_session = model.start_chat(history=st.session_state.hist)

        response = chat_session.send_message(user_message)

        st.session_state.hist.append({"role": "user", "parts": [user_message]})
        st.session_state.hist.append({"role": "model", "parts": [response.text]})

        return f"Bridgit: {response.text}"

    # Initialize the user's credits if not already set
    if "credits" not in st.session_state:
        st.session_state["credits"] = 100

    st.sidebar.header(f"Credits: {st.session_state['credits']}")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("You: "):
        if st.session_state['credits'] > 0:
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            st.session_state['credits'] -= 5

            response = bot_reply(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error('Looks like you are out of credits... ', icon="🚨")
