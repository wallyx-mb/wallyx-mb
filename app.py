import streamlit as st
import json
import os
from datetime import datetime

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
