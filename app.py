import streamlit as st
import google.generativeai as genai

# Page Title
st.set_page_config(page_title="AI GK Guru", page_icon="🤖")
st.title("🤖 AI GK Guru (Hindi)")

# 1. API Setup
# Best practice: API Key ko sidebar mein ya secrets mein rakhein
api_key = st.sidebar.text_input("Apni Gemini API Key Dalein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 2. Topic Input
    topic = st.text_input("Kis topic par GK chahiye?", placeholder="e.g. Space, India, Cricket")

    if st.button("GK Batao!"):
        if topic:
            try:
                with st.spinner('AI soch raha hai...'):
                    # Yahan hum sabse stable model use kar rahe hain
                    model = genai.GenerativeModel('gemini-1.5-flash') 
                    # Note: Agar 1.5-flash abhi bhi 404 de, toh yahan 'gemini-2.0-flash' likh dein.
                    
                    response = model.generate_content(f"Give me an amazing GK fact about {topic} in Hindi.")
                    
                    st.success("Done!")
                    st.subheader(f"Fact about {topic}:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Ek error aaya: {e}")
        else:
            st.warning("Pehle koi topic toh likho bhai!")
else:
    st.info("Side mein apni API Key daalein shuru karne ke liye.")

# Footer
st.markdown("---")
st.caption("Powered by Gemini AI | 2026 Edition")
