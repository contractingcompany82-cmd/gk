import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="GK AI Guru", page_icon="🎓")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- API KEY SETUP ---
# Aap sidebar mein key daal sakte hain ya code mein fix kar sakte hain
with st.sidebar:
    st.title("⚙️ AI Control Room")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Key yahan se lein: https://aistudio.google.com/app/apikey")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- INITIALIZE AI ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("Bhai, pehle Sidebar mein API Key daalo!")
    st.stop()

# --- CHAT INTERFACE ---
st.title("🎓 GK AI Guru")
st.caption("Main General Knowledge ka expert hoon. Kuch bhi puchein!")

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Duniya ka sabse uncha pahad kaunsa hai?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                # System Instruction for GK focus
                full_prompt = f"You are a GK Expert. Answer in short and clear points. Question: {prompt}"
                response = model.generate_content(full_prompt)
                answer = response.text
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")
