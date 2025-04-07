# Notebook: Lebensstil-Daten analysieren per Kommandozeilen-Argumente

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import sys

# Argumente definieren
parser = argparse.ArgumentParser(description="Erstelle verschiedene Plots zur Lebensstil-CSV-Datei.")
parser.add_argument("plottyp", help="Welche Art von Plot soll erstellt werden? Optionen: bmi, zucker, alkohol, sport, raucher_sport, sozialstatus, geschlecht, help")
args = parser.parse_args()

# Hilfe-Option manuell behandeln
if args.plottyp == "help":
    print("\nVerfügbare Plot-Typen:")
    print("  bmi             - Scatterplot: BMI vs. Alter")
    print("  zucker          - Balkendiagramm: Zuckerkonsum vs. Alter")
    print("  alkohol         - Boxplot: Alkoholkonsum vs. Alter")
    print("  sport           - Violinplot: Sportverhalten vs. Alter")
    print("  raucher_sport   - Gruppierter Balkenplot: Rauchen & Sport")
    print("  sozialstatus    - Balkendiagramm: Sozialstatus vs. Alter")
    print("  geschlecht      - Boxplot: Geschlecht vs. Alter")
    sys.exit()

# Daten laden
df = pd.read_csv("lebensstil_experiment.csv")

# Plot-Auswahl
if args.plottyp == "bmi":
    sns.scatterplot(data=df, x="BMI", y="Alter_beim_Tod", hue="Raucher")
    plt.title("BMI vs. Alter beim Tod")

elif args.plottyp == "zucker":
    df.groupby("Zuckerkonsum")["Alter_beim_Tod"].mean().plot(kind="bar")
    plt.title("Durchschnittliches Alter nach Zuckerkonsum")
    plt.ylabel("Alter beim Tod")

elif args.plottyp == "alkohol":
    sns.boxplot(data=df, x="Alkoholkonsum", y="Alter_beim_Tod")
    plt.title("Sterbealter nach Alkoholkonsum")

elif args.plottyp == "sport":
    sns.violinplot(data=df, x="Sport", y="Alter_beim_Tod")
    plt.title("Sportverhalten vs. Lebensalter")

elif args.plottyp == "raucher_sport":
    sns.barplot(data=df, x="Raucher", y="Alter_beim_Tod", hue="Sport")
    plt.title("Sterbealter nach Raucherstatus und Sport")

elif args.plottyp == "sozialstatus":
    df.groupby("Sozialstatus")["Alter_beim_Tod"].mean().plot(kind="bar")
    plt.title("Sterbealter nach Sozialstatus")
    plt.ylabel("Alter beim Tod")

elif args.plottyp == "geschlecht":
    sns.boxplot(data=df, x="Geschlecht", y="Alter_beim_Tod")
    plt.title("Sterbealter nach Geschlecht")

else:
    print("Ungültiger Plot-Typ. Verwende: help")
    sys.exit()

plt.tight_layout()
plt.show()
