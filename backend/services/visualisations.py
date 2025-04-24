
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Compatibilité Streamlit et exécution locale
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "donnees_nettoyees.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "visuels")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generer_graphiques():
    df = pd.read_csv(DATA_PATH)

    # ✅ 1. Évolution des flux commerciaux
    df_flux = df.groupby(["Année", "Flux"])["Montant"].sum().unstack()
    df_flux.plot(kind="bar", figsize=(10, 5), title="Évolution des Flux")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "evolution_flux.png"))
    plt.close()

    # ✅ 2. Top 10 Produits tous flux confondus
    top_produits = (
        df.groupby("Produit")["Montant"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    top_produits.plot(kind="barh", figsize=(8, 5), title="Top 10 Produits")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_produits.png"))
    plt.close()

    # ✅ 3. Barres empilées par année
    montant_par_annee = df.groupby(["Année", "Flux"])["Montant"].sum().unstack().fillna(0)
    montant_par_annee.plot(kind="bar", stacked=True, figsize=(10, 5), title="Montant total échangé par année")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "montant_par_annee.png"))
    plt.close()

    # ✅ 4. Heatmap produit/année
    produit_annee = df.pivot_table(index="Produit", columns="Année", values="Montant", aggfunc="sum").fillna(0)
    top_20_produits = produit_annee.sum(axis=1).sort_values(ascending=False).head(20).index
    plt.figure(figsize=(12, 10))
    sns.heatmap(produit_annee.loc[top_20_produits], cmap="YlGnBu", linewidths=0.5)
    plt.title("Heatmap des montants par produit et par année")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "heatmap_produits_annees.png"))
    plt.close()

    # ✅ 5. Courbe des top 5 produits dans le temps
    top5 = df.groupby("Produit")["Montant"].sum().sort_values(ascending=False).head(5).index
    top5_df = df[df["Produit"].isin(top5)]
    evolution_top5 = top5_df.groupby(["Année", "Produit"])["Montant"].sum().unstack().fillna(0)
    evolution_top5.plot(figsize=(10, 5), title="Évolution du Top 5 Produits")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "evolution_top5.png"))
    plt.close()

if __name__ == "__main__":
    generer_graphiques()
    print("✅ Tous les visuels ont été générés dans /data/visuels")
