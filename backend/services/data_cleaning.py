
import pandas as pd
import os

# ✅ Chemin absolu basé sur l'emplacement du fichier courant
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(BASE_DIR, "data", "donnees_brutes.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "donnees_nettoyees.csv")

def nettoyer_donnees():
    df = pd.read_csv(DATA_PATH)

    colonnes_essentielles = ["Produit", "Flux", "Date"]
    df = df.dropna(subset=colonnes_essentielles)

    if df["Montant"].isna().sum() > 0:
        mediane_montant = df["Montant"].median()
        df.loc[:, "Montant"] = df["Montant"].fillna(mediane_montant)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Année"] = df["Date"].dt.year

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    return df

if __name__ == "__main__":
    df_resultat = nettoyer_donnees()
    print("✅ Données nettoyées. Aperçu :")
    print(df_resultat.head())
