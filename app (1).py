
import streamlit as st
import json
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Agenda Familial 👨‍👩‍👧‍👦",
    page_icon="📅",
    layout="centered"
)

st.markdown(
    """
    <div style='text-align: center; padding: 25px; background-color: #1f2937; border-radius: 16px;'>
        <h1 style='font-size: 36px; color: #f9fafb;'>📅 Agenda de la famille Mbuyi</h1>
        <p style='font-size: 16px; color: #9ca3af;'>Organisez les moments importants, tous au même endroit 🤍</p>
    </div>
    """,
    unsafe_allow_html=True
)

MOT_DE_PASSE = "famille123"

if "authentifie" not in st.session_state:
    st.session_state.authentifie = False

if not st.session_state.authentifie:
    mdp = st.text_input("🔒 Entrez le mot de passe", type="password")
    if mdp == MOT_DE_PASSE:
        st.success("🔓 Accès autorisé")
        st.session_state.authentifie = True
        st.rerun()
    elif mdp != "":
        st.error("Mot de passe incorrect")
    st.stop()

FICHIER_EVENTS = "evenements.json"

def charger_evenements():
    if os.path.exists(FICHIER_EVENTS):
        with open(FICHIER_EVENTS, "r") as f:
            return json.load(f)
    return []

def enregistrer_evenements(evenements):
    with open(FICHIER_EVENTS, "w") as f:
        json.dump(evenements, f, indent=2)

evenements = charger_evenements()

st.subheader("🔔 Rappels")
auj = datetime.today().date()
a_venir = [e for e in evenements if auj <= datetime.strptime(e["date"], "%Y-%m-%d").date() <= auj + timedelta(days=2)]
if a_venir:
    for e in a_venir:
        st.warning(f"🔔 Rappel : **{e['titre']}** est prévu le {e['date']} !")
else:
    st.info("Aucun événement imminent.")

st.subheader("➕ Ajouter / Modifier un événement")

if "mode_edition" not in st.session_state:
    st.session_state.mode_edition = False
if "index_modif" not in st.session_state:
    st.session_state.index_modif = -1

with st.form("ajout_event"):
    titre = st.text_input("Titre", value=evenements[st.session_state.index_modif]["titre"] if st.session_state.mode_edition else "")
    date = st.date_input("Date", value=datetime.strptime(evenements[st.session_state.index_modif]["date"], "%Y-%m-%d").date() if st.session_state.mode_edition else datetime.today())
    description = st.text_area("Description", value=evenements[st.session_state.index_modif]["description"] if st.session_state.mode_edition else "")

    submit = st.form_submit_button("✅ Enregistrer")
    if submit:
        nouvel_event = {
            "titre": titre,
            "date": date.strftime("%Y-%m-%d"),
            "description": description
        }
        if st.session_state.mode_edition:
            evenements[st.session_state.index_modif] = nouvel_event
            st.success("✏️ Événement modifié.")
        else:
            evenements.append(nouvel_event)
            st.success("📌 Événement ajouté.")
        enregistrer_evenements(evenements)
        st.session_state.mode_edition = False
        st.session_state.index_modif = -1
        st.rerun()

st.subheader("📆 Calendrier du mois")

evenements = sorted(evenements, key=lambda e: e["date"])
mois_actuel = datetime.today().strftime("%Y-%m")
for i, e in enumerate(evenements):
    if e["date"].startswith(mois_actuel):
        with st.expander(f"{e['date']} – {e['titre']}"):
            st.write(e["description"])
            col1, col2 = st.columns(2)
            if col1.button("✏️ Modifier", key=f"modif_{i}"):
                st.session_state.mode_edition = True
                st.session_state.index_modif = i
                st.rerun()
            if col2.button("🗑 Supprimer", key=f"suppr_{i}"):
                evenements.pop(i)
                enregistrer_evenements(evenements)
                st.success("Événement supprimé.")
                st.rerun()
