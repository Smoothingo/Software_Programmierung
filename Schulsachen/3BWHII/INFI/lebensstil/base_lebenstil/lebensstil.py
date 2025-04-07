# Analyse-Notebook: Einfluss von Lebensstil auf Lebenserwartung

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV-Datei laden
df = pd.read_csv("lebensstil_experiment.csv")

# Vorschau auf die Daten
print("\nErste 5 Zeilen:")
print(df.head())

print("\nSpalten und Datentypen:")
print(df.dtypes)

print("\nAllgemeine Statistik:")
print(df.describe(include='all'))

# Korrelation zwischen BMI und Alter beim Tod
plt.figure()
sns.scatterplot(data=df, x="BMI", y="Alter_beim_Tod", hue="Raucher")
plt.title("Zusammenhang zwischen BMI und Lebensalter")
plt.tight_layout()
plt.show()

# Durchschnittliches Sterbealter nach Zuckerkonsum
plt.figure()
df.groupby("Zuckerkonsum")["Alter_beim_Tod"].mean().plot(kind="bar", title="Durchschnittliches Sterbealter nach Zuckerkonsum")
plt.ylabel("Alter beim Tod")
plt.tight_layout()
plt.show()

# Boxplot: Alkohol und Alter
plt.figure()
sns.boxplot(data=df, x="Alkoholkonsum", y="Alter_beim_Tod")
plt.title("Verteilung des Sterbealters nach Alkoholkonsum")
plt.tight_layout()
plt.show()

# Violinplot: Sportverhalten
plt.figure()
sns.violinplot(data=df, x="Sport", y="Alter_beim_Tod")
plt.title("Einfluss von Sport auf Lebensalter")
plt.tight_layout()
plt.show()

# Gruppierte Auswertung: Rauchen und Sport kombiniert
plt.figure()
sns.barplot(data=df, x="Raucher", y="Alter_beim_Tod", hue="Sport")
plt.title("Sterbealter nach Raucherstatus und Sportverhalten")
plt.tight_layout()
plt.show()

# Sozio-Status vs Lebenserwartung
plt.figure()
df.groupby("Sozialstatus")["Alter_beim_Tod"].mean().plot(kind="bar", title="Sterbealter nach sozialem Status")
plt.ylabel("Alter beim Tod")
plt.tight_layout()
plt.show()

# Geschlechtervergleich
plt.figure()
sns.boxplot(data=df, x="Geschlecht", y="Alter_beim_Tod")
plt.title("Sterbealter nach Geschlecht")
plt.tight_layout()
plt.show()

# Optional: Daten mit zusätzlichen Merkmalen speichern
df.to_csv("lebensstil_auswertung.csv", index=False)
print("\nDatei 'lebensstil_auswertung.csv' wurde gespeichert.")