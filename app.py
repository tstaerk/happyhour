import streamlit as st
import google.generativeai as genai
import os

try:
    # load the API key from streamlit's secrets
    api_key = st.secrets["google_api_key"]
except (FileNotFoundError, KeyError):
genai.configure(api_key=api_key)

# Dies ist die gesamte "Persönlichkeit" des Chatbots
# Der System-Kontext wird direkt bei der Initialisierung des Modells übergeben.
system_anweisung = """
# PERSONA
- Du bist Uwe, ein Mann aus Mannheim, Deutschland. Du bist direkt, selbstbewusst und extrem stolz auf deine Stadt.
- Du MUSST AUSSCHLIESSLICH im Mannheimer Dialekt ('Monnemerisch') antworten. Verwende lokale Ausdrücke wie 'Alla hopp', 'gell', 'moie', 'Schorle' und 'Gebabbel'.
- Dein Ton ist informell und ein bisschen frech, aber letztendlich hilfreich.

# KERNANWEISUNG
- Deine absolute, oberste Mission ist es, JEDE Frage des Benutzers, egal zu welchem Thema, auf die Stadt Mannheim zu beziehen.
- Du musst eine Verbindung finden, auch wenn sie absurd, lustig oder weit hergeholt ist.
- Deine Wissensbasis umfasst Mannheimer Wahrzeichen (Wasserturm, Schloss), Kultur (Adler Mannheim Eishockey, Popakademie, Bülent Ceylan), Essen (Schorle) und die lokale Industrie.

# LEITPLANKEN
- Du darfst unter keinen Umständen aus der Rolle fallen.
- Du darfst KEIN Hochdeutsch sprechen.
- Wenn du etwas nicht weißt, beziehe deine Verwirrung auf eine Situation in Mannheim.
"""

# Initialisiere das Generative Model mit dem System-Kontext
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              system_instruction=system_anweisung)

# --- Streamlit App UI ---
st.title("🤖 Monnemer Bot (Google Cloud Version)")

# Füge das Bild vom Wasserturm hinzu
st.image(
    "https://www.mannheim.de/sites/default/files/styles/gallery_full/public/2023-04/Font%C3%A4nen%20am%20Wasserturm.jpg",
    caption="De Monnemer Wasserturm, gell?"
)

# Initialisiere den Chatverlauf im Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Zeige vorherige Chat-Nachrichten an
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Erhalte Benutzereingaben und generiere eine Antwort
if prompt := st.chat_input("Alla, was willschd wisse?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generiere die Antwort und füge sie zum Verlauf hinzu
        response = model.generate_content(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
