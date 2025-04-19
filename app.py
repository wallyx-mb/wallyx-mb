# Nouveau planning hebdomadaire type emploi du temps dans Streamlit

import streamlit as st
import json
from datetime import datetime
import os

st.set_page_config(
    page_title="Agenda de la famille Mbuyi",
    page_icon="📅",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center;'>📅 Agenda de la famille Mbuyi</h1>
    <p style='text-align: center;'>Organisez les moments importants, tous au même endroit 💖</p>
""", unsafe_allow_html=True)

MOT_DE_PASSE = "famille123"

if "acces_autorise" not in st.session_state:
    mot_de_passe = st.text_input("Entrez le mot de passe", type="password")
    if mot_de_passe == MOT_DE_PASSE:
        st.session_state.acces_autorise = True
        st.rerun()
    else:
        st.stop()

# Chargement des événements
DATA_PATH = "evenements.json"
def charger_evenements():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []

def sauvegarder_evenements(evenements):
    with open(DATA_PATH, "w") as f:
        json.dump(evenements, f, indent=2)

evenements = charger_evenements()

# Interface ajout d'événement
st.subheader("➕ Ajouter / Modifier un événement")
col1, col2, col3 = st.columns(3)
titre = col1.text_input("Titre")
date = col2.date_input("Date", value=datetime.today())
heure = col3.selectbox("Heure", ["8h-10h", "10h-12h", "12h-14h", "14h-16h", "16h-18h"])
description = st.text_area("Description")
couleur = st.color_picker("Couleur de l'événement", "#1E90FF")

if st.button("✅ Enregistrer"):
    evenements.append({
        "titre": titre,
        "date": str(date),
        "heure": heure,
        "description": description,
        "couleur": couleur
    })
    sauvegarder_evenements(evenements)
    st.success("Événement enregistré avec succès")

# Planning esthétique (tableau)
st.subheader("📚 Planning hebdomadaire esthétique")
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
horaires = ["8h-10h", "10h-12h", "12h-14h", "14h-16h", "16h-18h"]

# Création du tableau
html = """
<table style='width:100%; border-collapse: collapse;'>
    <tr style='background-color: #f9f9f9;'>
        <th style='border: 1px solid #ccc; padding: 8px;'>Horaire</th>"""
for jour in jours:
    html += f"<th style='border: 1px solid #ccc; padding: 8px;'>{jour}</th>"
html += "</tr>"

for h in horaires:
    html += f"<tr><td style='border: 1px solid #ccc; padding: 8px;'>{h}</td>"
    for j in jours:
        cell = ""
        for evt in evenements:
            evt_date = datetime.strptime(evt["date"], "%Y-%m-%d")
            if evt_date.strftime("%A").lower() == j.lower() and evt["heure"] == h:
                cell = f"<div style='background-color:{evt['couleur']}; padding:5px; border-radius:6px;'>{evt['titre']}</div>"
        html += f"<td style='border: 1px solid #ccc; padding: 8px; text-align: center;'>{cell}</td>"
    html += "</tr>"
html += "</table>"

st.markdown(html, unsafe_allow_html=True)
