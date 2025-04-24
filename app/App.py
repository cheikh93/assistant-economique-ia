import streamlit as st

st.set_page_config(
    page_title="Assistant Éco Sénégal",
    page_icon="🇸🇳",
    layout="wide"
)

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Flag_of_Senegal.svg/640px-Flag_of_Senegal.svg.png", width=80)
    st.title("📚 Navigation")
    st.page_link("pages/1_📂_Nettoyage.py", label="Nettoyage", icon="🧹")
    st.page_link("pages/2_📊_Visualisations.py", label="Visualisations", icon="📈")
    st.page_link("pages/3_📄_Rapport.py", label="Rapport", icon="📄")
    st.page_link("pages/4_🤖_Chatbot.py", label="Chatbot", icon="🤖")

st.title("🇸🇳 Assistant Économique du Sénégal")
st.subheader("Bienvenue dans votre tableau de bord interactif")
st.write("""
Ce tableau de bord vous permet :
- 🧹 de nettoyer vos données
- 📊 de les visualiser
- 📄 de générer un rapport
- 🤖 de poser des questions en langage naturel

👈 Utilisez la barre latérale pour commencer.
""")
st.success("✅ Interface complète prête à l’emploi.")
