import google.generativeai as genai
import sys

# 1. API Setup
API_KEY = "YOUR_API_KEY_HERE"  # <--- Apna real API key yahan dalein
genai.configure(api_key=API_KEY)

# 2. Model Selection (2026 Latest)
# Agar ye error de, toh 'gemini-2.5-flash' try karein
MODEL_NAME = 'gemini-3-flash' 

print(f"--- AI GK Bot Start Ho Raha Hai (Model: {MODEL_NAME}) ---")

try:
    model = genai.GenerativeModel(MODEL_NAME)
    
    # Input prompt
    topic = input("Aap kis topic ke baare mein jaanna chahte hain? (Type karke Enter dabayein): ")
    
    if not topic:
        print("Bhai, kuch topic toh likho!")
        sys.exit()

    print(f"\nSawaal: {topic} ke baare mein soch raha hoon... thoda rukiye...")

    # Response generation
    response = model.generate_content(f"Give me an amazing GK fact about {topic} in Hindi.")
    
    print("-" * 30)
    print("YE RAHA RESULT:")
    print(response.text)
    print("-" * 30)

except Exception as e:
    print(f"\n[ERROR]: Kuch gadbad ho gayi!")
    print(f"Details: {e}")

input("\nProgram band karne ke liye Enter dabayein...")
