import streamlit as st
import requests

# ==========================================
# API Configuration
# ==========================================

BASE_URL = "http://127.0.0.1:8000"

CHAT_URL = f"{BASE_URL}/chat"
HISTORY_URL = f"{BASE_URL}/history"
CLEAR_URL = f"{BASE_URL}/clear"
HEALTH_URL = f"{BASE_URL}/health"


# ==========================================
# API Functions
# ==========================================

def send_message(message: str):
    payload = {"message": message}
    return requests.post(CHAT_URL, json=payload, timeout=30)


def load_history():
    return requests.get(HISTORY_URL, timeout=10)


def clear_conversation():
    return requests.post(CLEAR_URL, timeout=10)


def check_backend():
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")


# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.header("Settings")

    if check_backend():
        st.success("🟢 Backend Connected")
    else:
        st.error("🔴 Backend Offline")

    if st.button("🗑 Clear Conversation"):

        try:
            clear_conversation()
        except Exception:
            pass

        st.session_state.messages = []

        st.rerun()


# ==========================================
# Load Previous History
# ==========================================

if "messages" not in st.session_state:

    try:

        response = load_history()

        if response.status_code == 200:

            data = response.json()

            st.session_state.messages = data.get(
                "history",
                []
            )

        else:

            st.session_state.messages = []

    except Exception:

        st.session_state.messages = []


# ==========================================
# Display Chat History
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# Chat Input
# ==========================================

prompt = st.chat_input("Type your message here...")

if prompt:

    # Show user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = send_message(prompt)

                if response.status_code == 200:

                    data = response.json()

                    bot_reply = data.get(
                        "response",
                        "No response returned."
                    )

                    st.markdown(bot_reply)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": bot_reply
                        }
                    )

                else:

                    try:
                        error_detail = response.json().get(
                            "detail",
                            f"Server error ({response.status_code})"
                        )
                    except Exception:
                        error_detail = f"Server error ({response.status_code})"

                    st.error(error_detail)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the backend server."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱ Backend request timed out."
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )