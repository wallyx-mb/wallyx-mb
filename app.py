import streamlit as st
import json
import os
from datetime import datetime
st.set_page_config(
    page_title="Agenda Familial 👨‍👩‍👧‍👦",
    page_icon="📅",
    layout="centered",  # ou "wide" si tu veux un affichage plein écran
)
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 12px;'>
        <h1 style='color:#2c3e50;'>👨‍👩‍👧‍👦 Bienvenue sur l'agenda de la famille Mbuyi !</h1>
        <p style='font-size:18px; color:#555;'>Planifiez, partagez, et profitez de chaque moment ensemble 💖</p>
    </div>
    """,
    unsafe_allow_html=True
)

FICHIER_EVENTS = "evenements.json"

# Charger les événements existants
def charger_evenements():
    if os.path.exists(FICHIER_EVENTS):
        with open(FICHIER_EVENTS, "r") as f:
            return json.load(f)
    return []

# Enregistrer les événements
def enregistrer_evenements(evenements):
    with open(FICHIER_EVENTS, "w") as f:
        json.dump(evenements, f, indent=2)

# Interface Streamlit
st.title("📅 Agenda Familial")

# Formulaire pour ajouter un événement
with st.form("ajouter_event"):
    titre = st.text_input("Titre de l'événement")
    date = st.date_input("Date")
    description = st.text_area("Description")

    soumettre = st.form_submit_button("Ajouter")

    if soumettre:
        evenements = charger_evenements()
        evenements.append({
            "titre": titre,
            "date": date.strftime("%Y-%m-%d"),
            "description": description
        })
        enregistrer_evenements(evenements)
        st.success("Événement ajouté avec succès !")

# Afficher la liste des événements
st.subheader("📆 Événements à venir")
evenements = charger_evenements()
evenements = sorted(evenements, key=lambda e: e["date"])


for i, event in enumerate(evenements):
    with st.expander(f"📌 {event['titre']} – {event['date']}"):
        st.write(event["description"])
        if st.button(f"🗑 Supprimer", key=f"supprimer_{i}"):
            evenements.pop(i)
            enregistrer_evenements(evenements)
            st.success("Événement supprimé !")
            st.experimental_rerun()
# Mot de passe de la famille
MOT_DE_PASSE = "owenfamily"

if "authentifie" not in st.session_state:
    st.session_state.authentifie = False

if not st.session_state.authentifie:
    mdp = st.text_input("🔒 Entrez le mot de passe", type="password")
    if mdp == MOT_DE_PASSE:
        st.success("🔓 Accès autorisé")
        st.session_state.authentifie = True
        st.experimental_rerun()
    elif mdp != "":
        st.error("Mot de passe incorrect")
    st.stop()  # Stoppe l'app si pas authentifié
