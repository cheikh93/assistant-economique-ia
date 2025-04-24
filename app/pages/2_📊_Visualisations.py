
import streamlit as st
import os
import sys

try:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from backend.services.visualisations import generer_graphiques

st.set_page_config(page_title="📊 Visualisations", page_icon="📊")
st.title("📊 Visualisation des échanges commerciaux")

if st.button("Générer les graphiques"):
    generer_graphiques()
    st.success("✅ Graphiques générés avec succès !")

    visuels_dir = os.path.join(base_dir, "data", "visuels")

    st.header("1️⃣ Évolution des flux commerciaux")
    st.image(os.path.join(visuels_dir, "evolution_flux.png"))

    st.header("2️⃣ Top 10 des produits")
    st.image(os.path.join(visuels_dir, "top_produits.png"))

    st.header("3️⃣ Barres empilées par année")
    st.image(os.path.join(visuels_dir, "montant_par_annee.png"))

    st.header("4️⃣ Heatmap des produits par année")
    st.image(os.path.join(visuels_dir, "heatmap_produits_annees.png"))

    st.header("5️⃣ Évolution du Top 5 produits")
    st.image(os.path.join(visuels_dir, "evolution_top5.png"))
