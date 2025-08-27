import streamlit as st
import gdown
import os
import time
import random
from gensim.models import KeyedVectors
import gensim.downloader as api


# File settings
MODEL_PATH = "envectors.bin"
GOOGLE_DRIVE_ID = "166uEsVxPv1jD_qnv8y9w9B1pFZFUHCMM"

# ✩ Reactions and mascotte images
reactions = {
    "loading": [
        "Hmm... I'm thinking...",
        "Patience...",
        "My circuits are heating up a bit, please wait"
    ],
    "win": [
        "Oh yeah!",
        "You won!",
        "Full house!"
    ],
    "fail": [
        "Ouch...",
        "Nope, that doesn’t really fit",
        "Not a win this time!"
    ],
    "close": [
        "At this point it's not proximity, it's fusion",
        "Those two words are closer than two socks in a drawer",
        "Of course they're close... Bravo Sherlock",
        "Water is wet and fire burns..."
    ],
    "far": [
        "Like day and night... and apparently you're not the brightest...",
        "I'm shocked you even tried that... and I'm just an algorithm!",
        "That’s quite a lexical split"
    ]
}


images = {
    "loading": "mascotte_loading.png",
    "win": "mascotte_win.png",
    "fail": "mascotte_fail.png",
    "close": "mascotte_close.png",
    "far": "mascotte_far.png"
}

# Display mascotte image and message
def display_mascotte(state):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(images[state],width=200)
    with col2:
        phrase = random.choice(reactions[state])
        st.markdown(
            f"<div style='color: yellow; font-weight: bold; font-size: 18px;'>{phrase}</div>",
            unsafe_allow_html=True
        )

# 🔹 Download model
def download_model():
    msg = st.empty()
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 5000000:
        msg.info("Chargement du modèle...")
        url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        msg.success("Modèle chargé!")
        time.sleep(1.5)
    msg.empty()

# 🔹 Load model
@st.cache_resource
def load_model():
    download_model()
    try:
        return KeyedVectors.load_word2vec_format(MODEL_PATH, binary=True)
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        st.stop()

# 🔹 UI
st.set_page_config(page_title="Akinamot", layout="centered")


# col1, col2 = st.columns([1, 3])
# with col1:
#     st.image("mascotte.png",)
# with col2:
#     st.markdown(
#         """
#         <div style='color: white; font-weight: bold; font-size: 20px;'>
#             Bienvenue sur Akinamot !<br>Je suis là pour vous aider à comparer deux mots.
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

word1 = st.text_input("First word:").strip().lower()
word2 = st.text_input("Second word:").strip().lower()
THRESHOLD = 0.215

if st.button("Are they close ?"):
    if word1 and word2:
        model = load_model()

        try:
            similarity = model.similarity(word1, word2)

            mascotte_placeholder = st.empty()
            with mascotte_placeholder.container():
                display_mascotte("loading")

            flicker_placeholder = st.empty()

            st.markdown(
                """
                <style>
                @keyframes fadeInOut {
                    0% { opacity: 1; }
                    50% { opacity: 0.2; }
                    100% { opacity: 1; }
                }
                .flicker {
                    animation: fadeInOut 0.4s infinite alternate;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            start_time = time.time()
            flicker_choices = [("YES", "#34D399"), ("NO", "#EF4444")]
            while time.time() - start_time < 5:
                text, color = random.choice(flicker_choices)
                flicker_placeholder.markdown(
                    f"""
                    <div class='flicker' style='background-color: {color}; padding: 25px; text-align: center; font-size: 36px; color: white; font-weight: bold; margin-top: 10px;'>
                        {text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                time.sleep(0.4)

            flicker_placeholder.empty()
            mascotte_placeholder.empty()

            # Choisir la réaction
            if similarity > 0.4:
                state = "close"
            elif similarity > THRESHOLD:
                state = "win"
            elif similarity < 0.09:
                state = "far"
            else:
                state = "fail"

            with mascotte_placeholder.container():
                display_mascotte(state)

            final_color = "#34D399" if similarity > THRESHOLD else "#EF4444"
            result = "YES" if similarity > THRESHOLD else "NO"

            st.markdown(
                f"""
                <div style='background-color: {final_color}; padding: 25px; text-align: center; font-size: 42px; color: white; font-weight: bold; margin-top: 10px;'>
                    {result}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(f"**Similarity score:** `{similarity:.3f}` (Seuil: {THRESHOLD})")

        except KeyError:
            st.error("Word not found")
    else:
        st.warning("Empty fields")