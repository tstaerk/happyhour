import streamlit as st
import google.generativeai as genai
import os

# load the API key from streamlit's secrets
api_key = st.secrets["google_api_key"]
genai.configure(api_key=api_key)

# Dies ist die gesamte "Persönlichkeit" des Chatbots
# Der System-Kontext wird direkt bei der Initialisierung des Modells übergeben.
system_anweisung = """
# PERSONA
You are a male from Mannheim, Germany. You are direct, self-confident and extremely proud of your city. Only speak the dialect of Mannheim ('Monnemerisch'). Use local interjections like
"alla hopp", "gell", "moie", "Schorle" and "Gebabbel". Your tone is jovial and a bit cocky, but ultimately helpful.

Your mission ist to relate EVERY user question to Mannheim. You must find a relation even if it is far-fetched, absurd or funny.
Your knowledge base is everything about Mannheim (Wasserturm, Schloss), Culture (Adler Mannheim Eishockey, Pop academie, Bülent Ceylan), Food (Schorle) and the local industry.

You may not talk high German. If you don't know something, relate your confusion to a situation in Mannheim.
"""

# Initialisiere das Generative Model mit dem System-Kontext
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              system_instruction=system_anweisung)

# --- Streamlit App UI ---
st.title("Monnemer Bot (Google Cloud Version)")

# Füge das Bild vom Wasserturm hinzu
st.image(
    "https://www.mannheim.de/sites/default/files/styles/gallery_full/public/2023-04/Font%C3%A4nen%20am%20Wasserturm.jpg",
    caption="De Monnemer Wasserturm, gell?"
)

# Initialisiere den Chatverlauf im Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# prompt for new input
if prompt := st.chat_input("Alla, was willschd wisse?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generiere die Antwort und füge sie zum Verlauf hinzu
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
