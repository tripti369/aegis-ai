import streamlit as st
import requests

# Base configuration
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Chatbot")

# Sidebar with status and controls
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input field
if prompt := st.chat_input("Type your message here..."):
    # 1. Display and store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Fetch bot response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"message": prompt}
                response = requests.post(API_URL, json=payload, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data.get("response", "No response returned.")
                    
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    # Handle API error response (e.g., {"detail": "Message cannot be empty."})
                    try:
                        error_detail = response.json().get("detail", f"Server error ({response.status_code})")
                    except Exception:
                        error_detail = f"Server error ({response.status_code})"
                    
                    st.error(f"**API Error:** {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend server. Verify that `http://127.0.0.1:8000` is running.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The backend took too long to respond.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")