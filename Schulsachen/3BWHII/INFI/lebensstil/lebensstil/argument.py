import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import sys

# Argumente definieren
parser = argparse.ArgumentParser(description="Erstelle verschiedene Plots zur Lebensstil-CSV-Datei.")
parser.add_argument("datenspalte", help="Welche Daten sollen geplottet werden? Optionen: Alter_beim_Tod, Zuckerkonsum, Alkoholkonsum, BMI, Sozialstatus, Sport, Raucher, Geschlecht")
parser.add_argument("plotart", help="Art des Plots: scatter, bar, box, violin, grouped_bar")
args = parser.parse_args()

# Daten laden
df = pd.read_csv("lebensstil_experiment.csv")

# Prüfen, ob die ausgewählte Spalte existiert
if args.datenspalte not in df.columns:
    print(f"Ungültige Datenspalte. Verfügbare Optionen: {', '.join(df.columns)}")
    sys.exit()

# Wenn BMI geplottet wird, runde in 5er-Schritten
if args.datenspalte == "BMI":
    df[args.datenspalte] = df[args.datenspalte].apply(lambda x: round(x / 5) * 5)

# Plot erstellen
plt.figure(figsize=(8, 6))
if args.plotart == "scatter":
    sns.scatterplot(data=df, x=args.datenspalte, y="Alter_beim_Tod", hue=args.datenspalte, palette="Set1", legend=False)
elif args.plotart == "bar":
    sns.barplot(data=df, x=args.datenspalte, y="Alter_beim_Tod", hue=args.datenspalte, palette="Set1", legend=False)
elif args.plotart == "box":
    sns.boxplot(data=df, x=args.datenspalte, y="Alter_beim_Tod", hue=args.datenspalte, palette="Set1", legend=False)
elif args.plotart == "violin":
    sns.violinplot(data=df, x=args.datenspalte, y="Alter_beim_Tod", hue=args.datenspalte, palette="Set1", legend=False)
elif args.plotart == "grouped_bar":
    sns.barplot(data=df, x=args.datenspalte, y="Alter_beim_Tod", hue=args.datenspalte, palette="Set1", legend=False)
else:
    print("Ungültige Plot-Art. Verfügbare Optionen: scatter, bar, box, violin, grouped_bar")
    sys.exit()

plt.title(f"{args.datenspalte} vs. Alter beim Tod")
plt.tight_layout()
plt.show()
