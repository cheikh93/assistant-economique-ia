#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[15]:


import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# 🔐 Chargement des variables d'environnement
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ✅ Chemin robuste pour compatibilité Jupyter + Streamlit
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))

CSV_PATH = os.path.join(BASE_DIR, "data", "donnees_nettoyees.csv")

def charger_donnees():
    return pd.read_csv(CSV_PATH)

def extraire_contexte(question: str, df: pd.DataFrame) -> str:
    question_lower = question.lower()

    # 🔍 Filtrage par flux
    if "export" in question_lower:
        df = df[df["Flux"].str.contains("export", case=False)]
    elif "import" in question_lower:
        df = df[df["Flux"].str.contains("import", case=False)]

    # 🔍 Filtrage par année
    for annee in df["Année"].dropna().unique():
        if str(int(annee)) in question_lower:
            df = df[df["Année"] == int(annee)]

    # 🧮 Résumé des montants par produit
    resume = (
        df.groupby("Produit")["Montant"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    # 📜 Formatage du contexte pour GPT
    texte = "Produit\tMontant total (FCFA)\n"
    texte += "\n".join([f"{row['Produit']}\t{row['Montant']:.0f}" for _, row in resume.iterrows()])
    return texte

def generer_reponse_llm(question: str, contexte: str) -> str:
    prompt = f"""
    Tu es un expert économique du Sénégal. Réponds à la question suivante
    en te basant uniquement sur le CONTEXTE fourni :

    CONTEXTE :
    {contexte}

    QUESTION :
    {question}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un analyste économique du Sénégal."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur lors de la génération : {e}"

def poser_question_llm(question: str) -> str:
    df = charger_donnees()
    contexte = extraire_contexte(question, df)
    return generer_reponse_llm(question, contexte)


# In[16]:


import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# 🔐 Chargement des variables d'environnement
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ✅ Chemin robuste compatible Jupyter + Streamlit
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
except NameError:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))

CSV_PATH = os.path.join(BASE_DIR, "data", "donnees_nettoyees.csv")

def charger_donnees():
    return pd.read_csv(CSV_PATH)

def extraire_contexte(question: str, df: pd.DataFrame) -> str:
    question_lower = question.lower()
    df_filtre = df.copy()

    # 🔍 Filtrage flux
    if "export" in question_lower:
        df_filtre = df_filtre[df_filtre["Flux"].str.contains("export", case=False)]
    elif "import" in question_lower:
        df_filtre = df_filtre[df_filtre["Flux"].str.contains("import", case=False)]

    # 🔍 Filtrage années multiples
    annees = [int(mot) for mot in question_lower.split() if mot.isdigit() and 2000 <= int(mot) <= 2100]
    if annees:
        df_filtre = df_filtre[df_filtre["Année"].isin(annees)]

    # 🧮 Résumé
    resume = (
        df_filtre.groupby("Produit")["Montant"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    if resume.empty:
        return "Aucune donnée trouvée pour cette question."

    texte = "Produit\tMontant total (FCFA)\n"
    texte += "\n".join([f"{row['Produit']}\t{row['Montant']:.0f}" for _, row in resume.iterrows()])
    return texte

def generer_reponse_llm(question: str, contexte: str) -> str:
    prompt = f"""
    Tu es un assistant économique du Sénégal. Réponds à la question ci-dessous en te basant uniquement sur le CONTEXTE fourni.

    CONTEXTE :
    {contexte}

    QUESTION :
    {question}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en commerce international du Sénégal."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur lors de la génération : {e}"

def poser_question_llm(question: str) -> str:
    df = charger_donnees()
    contexte = extraire_contexte(question, df)
    return generer_reponse_llm(question, contexte)

# 🔁 Test local CLI
if __name__ == "__main__":
    print("🧪 Test du chatbot économique du Sénégal\n")
    while True:
        question = input("❓ Pose ta question (ou 'exit') : ")
        if question.lower() in ["exit", "quit", "q"]:
            break
        reponse = poser_question_llm(question)
        print("\n🤖 Réponse :\n")
        print(reponse)
        print("\n" + "="*60 + "\n")


# In[ ]:




