import streamlit as st
import requests
import json
# ==========================================
# API Configuration
# ==========================================

BASE_URL = "http://127.0.0.1:8000"

CHAT_URL = f"{BASE_URL}/chat"
HISTORY_URL = f"{BASE_URL}/history"
CLEAR_URL = f"{BASE_URL}/clear"
HEALTH_URL = f"{BASE_URL}/health"
MODE_URL = f"{BASE_URL}/mode"

STATS_URL = f"{BASE_URL}/stats"

# ==========================================
# API Helper Functions
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


def get_mode():
    return requests.get(MODE_URL, timeout=10)


def set_mode(mode: str):
    payload = {"mode": mode}
    return requests.post(MODE_URL, json=payload, timeout=10)

def get_stats():
    """
    Fetch chatbot statistics.
    """
    return requests.get(STATS_URL, timeout=10)

def export_chat_as_txt(messages):
    """
    Convert chat history into plain text.
    """
    lines = []

    for msg in messages:
        role = msg["role"].capitalize()
        content = msg["content"]

        lines.append(f"{role}:")
        lines.append(content)
        lines.append("-" * 50)

    return "\n".join(lines)

def export_chat_as_json(messages):
    """
    Convert chat history to JSON.
    """
    return json.dumps(messages, indent=4)


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
# Load Current Mode
# ==========================================

if "current_mode" not in st.session_state:

    try:
        response = get_mode()

        if response.status_code == 200:
            st.session_state.current_mode = response.json()["mode"]
        else:
            st.session_state.current_mode = "General"

    except Exception:
        st.session_state.current_mode = "General"


# ==========================================
# Load Previous Conversation
# ==========================================

if "messages" not in st.session_state:

    try:
        response = load_history()

        if response.status_code == 200:
            data = response.json()
            st.session_state.messages = data.get("history", [])

        else:
            st.session_state.messages = []

    except Exception:
        st.session_state.messages = []

stats = None

try:
    response = get_stats()

    if response.status_code == 200:
        stats = response.json()

except Exception:
    stats = None
# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.header("⚙️ Settings")

    # Backend Status
    if check_backend():
        st.success("🟢 Backend Connected")
    else:
        st.error("🔴 Backend Offline")

    st.divider()

    # Assistant Mode
    modes = [
        "General",
        "Coding",
        "Study",
        "Career"
    ]

    selected_mode = st.selectbox(
        "Assistant Mode",
        modes,
        index=modes.index(st.session_state.current_mode)
    )

    if selected_mode != st.session_state.current_mode:

        response = set_mode(selected_mode)

        if response.status_code == 200:
            st.session_state.current_mode = selected_mode
            st.success(f"Mode changed to {selected_mode}")
            st.rerun()
        else:
            st.error("Failed to change mode.")

    st.divider()

    # ==========================
    # Chat Statistics
    # ==========================

    st.subheader("📊 Chat Statistics")

    if stats:

        st.metric(
            "💬 Messages",
            stats["message_count"]
        )

        st.metric(
            "🎯 Current Mode",
            stats["mode"]
        )

        st.metric(
            "🧠 Memory Usage",
            f'{stats["message_count"]}/{stats["memory_limit"]}'
        )

        st.caption(
            f'🤖 Model: {stats["model"]}'
        )

    else:

        st.warning("Statistics unavailable.")

    st.divider()

    st.subheader("⬇ Export Conversation")

    txt_data = export_chat_as_txt(
      st.session_state.messages
)

    json_data = export_chat_as_json(
      st.session_state.messages
)

    st.download_button(
      label="📄 Download TXT",
      data=txt_data,
      file_name="chat_history.txt",
      mime="text/plain"
)

    st.download_button(
      label="📦 Download JSON",
      data=json_data,
      file_name="chat_history.json",
      mime="application/json"
)
    # Clear Conversation
    if st.button("🗑 Clear Conversation"):

        try:
            clear_conversation()
        except Exception:
            pass

        st.session_state.messages = []
        st.rerun()


# ==========================================
# Current Mode Display
# ==========================================

st.caption(
    f"🤖 Current Assistant Mode: **{st.session_state.current_mode}**"
)


# ==========================================
# Display Conversation
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==========================================
# Chat Input
# ==========================================

prompt = st.chat_input("Type your message here...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    st.rerun()

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

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
                            f"Server Error ({response.status_code})"
                        )

                    except Exception:
                        error_detail = f"Server Error ({response.status_code})"

                    st.error(error_detail)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the backend."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱ Backend request timed out."
                )

            except Exception as e:

                st.error(
                    f"Unexpected error:\n{e}"
                )