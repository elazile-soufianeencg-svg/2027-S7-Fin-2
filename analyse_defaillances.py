"""
Analyse des défaillances d'entreprises au Maroc (2022-2025).

Le script importe les 4 fichiers CSV du dossier data/ (chiffres Inforisk
repris par la presse économique marocaine), calcule les variations annuelles
et génère un graphique de synthèse (defaillances_maroc.png).

Usage :  python analyse_defaillances.py
Dépendances : pandas, matplotlib
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA = Path(__file__).parent / "data"
SORTIE = Path(__file__).parent / "defaillances_maroc.png"

# --- 1. Import des données -------------------------------------------------
annuel = pd.read_csv(DATA / "defaillances_annuelles.csv")
taille = pd.read_csv(DATA / "defaillances_par_taille.csv")
secteur = pd.read_csv(DATA / "defaillances_par_secteur_2024.csv")
ville = pd.read_csv(DATA / "defaillances_par_ville_2024.csv")

# --- 2. Calculs ------------------------------------------------------------
annuel = annuel.sort_values("annee")
annuel["variation_pct"] = annuel["defaillances"].pct_change() * 100
print("Défaillances annuelles et variation :")
print(annuel[["annee", "defaillances", "variation_pct"]].round(1).to_string(index=False))

# Nombre approximatif de défaillances par catégorie de taille en 2025
total_2025 = annuel.loc[annuel["annee"] == 2025, "defaillances"].iloc[0]
taille["nombre_approx"] = (taille["part_pct"] / 100 * total_2025).round()
print("\nRépartition par taille (2025) :")
print(taille[["categorie", "part_pct", "nombre_approx"]].to_string(index=False))

part_top4 = ville["part_pct"].sum()
print(f"\nCasablanca, Rabat, Tanger, Marrakech : {part_top4:.0f} % des défaillances 2024")

# --- 3. Graphique ----------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Défaillances d'entreprises au Maroc (source : Inforisk)", fontsize=14)

# a) évolution annuelle
ax = axes[0, 0]
barres = ax.bar(annuel["annee"].astype(str), annuel["defaillances"], color="#1f4e79")
for b, v in zip(barres, annuel["variation_pct"]):
    if pd.notna(v):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 150,
                f"{v:+.1f} %", ha="center", fontsize=9)
ax.set_ylim(0, annuel["defaillances"].max() * 1.15)
ax.set_title("Nombre de défaillances par an")
ax.set_ylabel("Entreprises")

# b) taille
ax = axes[0, 1]
ax.bar(taille["categorie"], taille["part_pct"], color=["#c0392b", "#e67e22", "#7f8c8d"])
for i, v in enumerate(taille["part_pct"]):
    ax.text(i, v + 1.5, f"{v} %", ha="center", fontsize=9)
ax.set_ylim(0, 110)
ax.set_title("Répartition par taille (2025)")
ax.set_ylabel("% des défaillances")

# c) secteur
ax = axes[1, 0]
s = secteur.sort_values("part_pct")
ax.barh(s["secteur"], s["part_pct"], color="#2e86c1")
for i, v in enumerate(s["part_pct"]):
    ax.text(v + 0.5, i, f"{v} %", va="center", fontsize=9)
ax.set_xlim(0, 40)
ax.set_title("Secteurs les plus touchés (2024)")
ax.set_xlabel("% des défaillances")

# d) ville
ax = axes[1, 1]
v = ville.sort_values("part_pct")
ax.barh(v["ville"], v["part_pct"], color="#117a65")
for i, val in enumerate(v["part_pct"]):
    ax.text(val + 0.4, i, f"{val} %", va="center", fontsize=9)
ax.set_xlim(0, 30)
ax.set_title("Villes les plus touchées (2024)")
ax.set_xlabel("% des défaillances")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(SORTIE, dpi=150)
print(f"\nGraphique enregistré : {SORTIE}")
