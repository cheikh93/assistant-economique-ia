
import streamlit as st
import os
import sys

try:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from backend.services.data_cleaning import nettoyer_donnees

st.set_page_config(page_title="🧹 Nettoyage des Données", page_icon="🧹")
st.title("🧹 Nettoyage des données brutes")

# ✅ Drapeau pour vérifier si les données ont été nettoyées
df = None

if st.button("Lancer le nettoyage"):
    df = nettoyer_donnees()
    st.success("✅ Données nettoyées avec succès !")
    st.dataframe(df.head())

    # ✅ Bouton de téléchargement
    st.download_button(
        label="📥 Télécharger les données complètes",
        data=df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="donnees_nettoyees.csv",
        mime="text/csv"
    )

st.markdown("Ce module permet de transformer les données brutes en un fichier nettoyé prêt à l'analyse.")
