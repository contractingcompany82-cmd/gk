import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI GK Guru", page_icon="🧠")
st.title("🧠 Smart AI GK Guru")

# Sidebar mein API Key
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- AUTO MODEL DETECT LOGIC ---
        # Hum check kar rahe hain ki aapke liye kaunsa model available hai
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority list: Jo mil jaye wahi sahi
        # Hum koshish karenge 2.0 ya 1.5 flash mil jaye
        selected_model = None
        for target in ['models/gemini-2.0-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']:
            if target in available_models:
                selected_model = target
                break
        
        if not selected_model and available_models:
            selected_model = available_models[0] # Jo bhi pehla mile wo uthalo
            
        st.sidebar.success(f"Connected to: {selected_model}")
        
        # --- UI INTERACTION ---
        topic = st.text_input("Topic ka naam likho (e.g. Maharana Pratap, Bitcoin, Mars):")

        if st.button("GK Batao!"):
            if topic and selected_model:
                try:
                    with st.spinner('AI data nikal raha hai...'):
                        model = genai.GenerativeModel(selected_model)
                        response = model.generate_content(f"Give me an amazing GK fact about {topic} in Hindi.")
                        
                        st.balloons()
                        st.subheader(f"Fact about {topic}:")
                        st.info(response.text)
                except Exception as e:
                    st.error(f"Generation Error: {e}")
            else:
                st.warning("Topic likhna zaroori hai!")

    except Exception as e:
        st.error(f"Connection Error: {e}. Shayad API Key galat hai?")
else:
    st.info("Bhai, pehle Sidebar mein API Key dalo!")
