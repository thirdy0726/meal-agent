import streamlit as st
from groq import Groq

# 1. Access the API Key securely from Streamlit's secrets
# (We will set this up later in the Streamlit dashboard)
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("API Key not found! Please set GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- UI Layout ---
st.set_page_config(page_title="AI Chef", page_icon="🍳")
st.title("👨‍🍳 Meal Suggestion Agent")
st.subheader("Turn your ingredients into a delicious recipe!")

# --- User Input ---
ingredients = st.text_input("What ingredients do you have?", placeholder="e.g., salmon, asparagus, lemon")

if st.button("Get Recipe"):
    if ingredients:
        with st.spinner("Chef is brainstorming..."):
            try:
                # 2. The Agent Logic
                system_msg = "You are a professional chef. Provide a Recipe Name and detailed, numbered cooking steps."
                user_msg = f"Suggest a recipe using: {ingredients}"

                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ]
                )
                
                # 3. Display the result
                st.success("Here is your recipe!")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please type some ingredients first!")