
import streamlit as st
import os
import sys
import base64

try:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from backend.services.report_generator import generer_rapport_complet

st.set_page_config(page_title="📄 Génération du Rapport", page_icon="📄")
st.title("📄 Génération automatique du rapport économique")

if st.button("Générer le rapport"):
    try:
        docx, pdf = generer_rapport_complet()
        st.success("✅ Rapport généré avec succès !")

        def telecharger_fichier(path, label):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:file/octet-stream;base64,{b64}" download="{os.path.basename(path)}">{label}</a>'
            st.markdown(href, unsafe_allow_html=True)

        if docx:
            telecharger_fichier(docx, "📄 Télécharger le rapport DOCX")

        if pdf:
            telecharger_fichier(pdf, "📄 Télécharger le rapport PDF")
        else:
            st.warning("⚠️ La conversion en PDF a échoué.")
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération : {e}")
