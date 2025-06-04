import os
import streamlit as st
import requests
import uuid

MODELS_ROOT = '/models'
API_URL = "http://api:5000/completion"
MAX_PROMPT_LENGTH = 1000

# --- Ambil model .gguf
gguf_files = []
for root, dirs, files in os.walk(MODELS_ROOT):
    for file in files:
        if file.endswith(".gguf"):
            gguf_files.append(os.path.join(root, file).replace("/models/", ""))

model_options = gguf_files if gguf_files else ["No models found"]

# --- Daftar persona manual (disesuaikan dengan backend)
persona_list = [
    "Musician Accountant",
    "Animal Lover Vet",
    "New Homeowner Lasagne",
    "Curious Child",
    "Loving Mother",
    "Technical Scientist"
]

# --- Session state init
if "rooms" not in st.session_state:
    st.session_state.rooms = {"default": []}

if "current_room" not in st.session_state:
    st.session_state.current_room = "default"

if "feedback" not in st.session_state:
    st.session_state.feedback = {"default": []}

if "selected_model" not in st.session_state:
    st.session_state.selected_model = model_options[0]

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = persona_list[0]

# --- Room function
def new_chat():
    new_id = str(uuid.uuid4())[:8]
    st.session_state.rooms[new_id] = []
    st.session_state.feedback[new_id] = []
    st.session_state.current_room = new_id
    return new_id

def select_room(room_id):
    st.session_state.current_room = room_id

def add_to_history(prompt, response):
    rid = st.session_state.current_room
    st.session_state.rooms[rid].append((prompt, response))
    st.session_state.feedback[rid].append(None)

def clear_chat():
    rid = st.session_state.current_room
    st.session_state.rooms[rid] = []
    st.session_state.feedback[rid] = []
    st.rerun()

def set_feedback(index, value):
    st.session_state.feedback[st.session_state.current_room][index] = value

# --- Sidebar (fokus riwayat)
with st.sidebar:
    st.title("💬 Chat Rooms")
    for room_id in st.session_state.rooms:
        label = f"Room {room_id}" if room_id != "default" else "Default Room"
        if st.button(label, key=room_id):
            select_room(room_id)
            st.rerun()

    if st.button("➕ New Chat"):
        new_chat()
        st.rerun()

    if st.button("🗑️ Delete Chat"):
        clear_chat()

# --- Header: Model & Persona Dropdown kanan atas
col_left, col_right = st.columns([4, 3])
with col_right:
    st.selectbox("🧠 Model", model_options, key="selected_model")
    st.selectbox("🧍 Persona", persona_list, key="selected_persona")

# --- Styling bubble chat
def render_chat():
    st.markdown("""
    <style>
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 12px;
        background-color: #f7f7fa;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease-in-out;
    }
    .user-bubble {
        background-color: #D1E8FF;
        color: #000;
        padding: 12px;
        margin: 8px 0;
        border-radius: 16px;
        text-align: left;
        margin-left: 25%;
        white-space: pre-wrap;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    .bot-bubble {
        background-color: #EAEAEA;
        color: #000;
        padding: 12px;
        margin: 8px 0;
        border-radius: 16px;
        text-align: left;
        margin-right: 25%;
        white-space: pre-wrap;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    .typing-indicator {
        font-style: italic;
        color: gray;
        padding-left: 10px;
        margin-top: -5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    room_id = st.session_state.current_room
    for i, (user_msg, bot_msg) in enumerate(st.session_state.rooms.get(room_id, [])):
        st.markdown(f'🧑‍💬 <div class="user-bubble">{user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'🤖 <div class="bot-bubble">{bot_msg}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 6])
        with col1:
            if st.button("👍", key=f"up_{i}"):
                set_feedback(i, "👍")
        with col2:
            if st.button("👎", key=f"down_{i}"):
                set_feedback(i, "👎")
        with col3:
            fb = st.session_state.feedback[room_id][i]
            if fb:
                st.write(f"Feedback: {fb}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Chat UI
st.title("🤖 Chat with LLM")

render_chat()

prompt = st.text_area("Ask anything:", height=100)

col1, col2 = st.columns([4, 1])
with col1:
    use_judol = st.checkbox("🛡️ Deteksi promosi judi")
    if use_judol and not ("wiki:" in prompt.lower() or "youtube.com" in prompt or "youtu.be" in prompt):
        st.info("🔍 Deteksi judi hanya aktif untuk prompt berisi komentar atau link YouTube.")

send_disabled = prompt.strip() == "" or st.session_state.selected_model == "No models found"

with col2:
    if st.button("Kirim", disabled=send_disabled):
        if len(prompt) > MAX_PROMPT_LENGTH:
            st.warning(f"Prompt terlalu panjang, maksimal {MAX_PROMPT_LENGTH} karakter.")
        else:
            try:
                if st.session_state.current_room == "default" and len(st.session_state.rooms.get("default", [])) == 0:
                    new_id = new_chat()
                    select_room(new_id)  # langsung masuk ke room baru

                with st.spinner("🤖 Sedang mengetik..."):
                    placeholder = st.empty()
                    placeholder.markdown('<div class="typing-indicator">🤖 Sedang mengetik...</div>', unsafe_allow_html=True)

                    response = requests.post(
                        API_URL,
                        json={
                            "model": st.session_state.selected_model,
                            "prompt": prompt,
                            "check_judi": use_judol,
                            "persona": st.session_state.selected_persona
                        },
                        timeout=300
                    )
                    placeholder.empty()

                if response.status_code == 200:
                    res_json = response.json()
                    result = res_json.get("response", "")
                    persona_used = res_json.get("persona_used")
                    if persona_used:
                        result += f"\n\n*(Persona: {persona_used})*"
                    add_to_history(prompt, result)
                    st.rerun()
                else:
                    try:
                        error_msg = response.json().get("error", f"HTTP {response.status_code} error")
                    except Exception:
                        error_msg = f"HTTP {response.status_code} error"
                    st.error(error_msg)
            except requests.Timeout:
                st.error("Timeout: Server terlalu lama merespon.")
            except requests.ConnectionError:
                st.error("Gagal koneksi ke server API.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
