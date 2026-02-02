import google.generativeai as genai

# Apna API Key yahan dalein
genai.configure(api_key="YOUR_API_KEY")

# Model ko update kiya gaya hai (1.5 se 2.5 ya 3-flash par)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gk_fact(topic):
    prompt = f"Give me an interesting GK fact about {topic} in Hindi."
    
    try:
        response = model.generate_content(prompt)
        print(f"GK Fact: {response.text}")
    except Exception as e:
        print(f"Oops! Ek error aaya: {e}")
        print("Tip: 'genai.list_models()' chala kar check karein ki aapke paas kaunsa model available hai.")

# Test karein
topic = input("Kis topic par GK chahiye? ")
get_gk_fact(topic)
