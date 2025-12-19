import streamlit as st
from groq import Groq

# API Setup
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Please set GROQ_API_KEY in Secrets.")
    st.stop()

# --- HEADER AND DESCRIPTION ---
st.set_page_config(page_title="AI Chef", page_icon="🍳")
st.title("👨‍🍳 Smart Chef Agent")

# Short description for the user
st.markdown("""
    **Welcome to your AI Kitchen Assistant!** This agent helps you turn leftovers or random pantry items into gourmet meals.  
    1. Enter your ingredients.  
    2. Get a custom recipe.  
    3. Ask for a different idea if you don't like the first one!
""")
st.info("I am powered by Llama 3.1 to provide creative, zero-waste cooking solutions.")

# Initialize Session State
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = ""
if 'recipe' not in st.session_state:
    st.session_state.recipe = ""

def get_recipe(ingredients):
    system_msg = "You are an expert chef. Suggest a UNIQUE recipe and detailed steps."
    user_msg = f"I have {ingredients}. Give me a recipe. If you've given one already, give a different one."
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
        temperature=0.8
    )
    st.session_state.recipe = completion.choices[0].message.content

# --- UI LOGIC ---

if not st.session_state.recipe:
    st.session_state.ingredients = st.text_input("What's in your fridge?", placeholder="e.g. eggs, tomato, bread")
    if st.button("Generate Recipe"):
        if st.session_state.ingredients:
            with st.spinner("Analyzing ingredients..."):
                get_recipe(st.session_state.ingredients)
            st.rerun()
else:
    st.markdown(st.session_state.recipe)
    st.markdown("---")
    
    st.write("### What would you like to do next?")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Different recipe (Same ingredients)"):
            get_recipe(st.session_state.ingredients)
            st.rerun()
            
    with col2:
        if st.button("🆕 Start over (New ingredients)"):
            st.session_state.recipe = ""
            st.session_state.ingredients = ""
            st.rerun()
            
    with col3:
        if st.button("✅ I'm done!"):
            st.balloons()
            st.success("Happy cooking!")
