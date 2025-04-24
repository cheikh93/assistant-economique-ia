#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os

# ✅ Gestion du chemin pour compatibilité Jupyter ET Streamlit
try:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
except NameError:
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import streamlit as st
from backend.services.chatbot import poser_question_llm
import pandas as pd
from datetime import datetime

# 📁 Fichier de log
LOG_PATH = os.path.join(base_dir, "outputs", "logs", "questions_log.csv")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# 🧠 Interface
st.set_page_config(page_title="🤖 Chatbot IA Sénégal", page_icon="🤖")
st.title("🤖 Assistant Économique - Sénégal")

question = st.text_input("Pose ta question sur les échanges commerciaux du Sénégal :")

if st.button("Envoyer") and question:
    with st.spinner("Analyse des données..."):
        reponse = poser_question_llm(question)

    # 📝 Affichage réponse
    st.markdown("### 💬 Réponse :")
    st.success(reponse)

    # 🗃️ Log question/réponse
    log_data = pd.DataFrame([[datetime.now(), question, reponse]], columns=["datetime", "question", "reponse"])
    if os.path.exists(LOG_PATH):
        log_data.to_csv(LOG_PATH, mode="a", header=False, index=False)
    else:
        log_data.to_csv(LOG_PATH, index=False)

# 📊 Historique optionnel
if st.checkbox("Afficher l'historique des questions"):
    if os.path.exists(LOG_PATH):
        historique = pd.read_csv(LOG_PATH)
        st.dataframe(historique.tail(10))
    else:
        st.info("Aucune question posée pour le moment.")


# In[ ]:




