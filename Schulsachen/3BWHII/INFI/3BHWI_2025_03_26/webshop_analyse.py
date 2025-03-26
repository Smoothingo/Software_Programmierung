# Online-Shop Verkaufsanalyse mit Pandas und Matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# Beispiel-Daten erstellen
daten = {
    'Bestellnummer': [1001, 1002, 1003, 1004, 1005, 1006],
    'Datum': ['2025-03-01', '2025-03-02', '2025-03-02', '2025-03-03', '2025-03-03', '2025-03-04'],
    'Produkt': ['T-Shirt', 'Hose', 'T-Shirt', 'Schuhe', 'Hose', 'Schuhe'],
    'Kategorie': ['Kleidung', 'Kleidung', 'Kleidung', 'Schuhe', 'Kleidung', 'Schuhe'],
    'Preis': [19.99, 39.99, 19.99, 59.99, 39.99, 59.99],
    'Anzahl': [2, 1, 3, 1, 2, 1]
}

# DataFrame erstellen
df = pd.DataFrame(daten)

# Datum in datetime umwandeln
df['Datum'] = pd.to_datetime(df['Datum'])

# Neue Spalte: Gesamtpreis
df['Gesamtpreis'] = df['Preis'] * df['Anzahl']

# Data anzeigen
print("\nDataFrame:")
print(df)

# Plot 1: Umsatz pro Kategorie
umsatz_kategorie = df.groupby('Kategorie')['Gesamtpreis'].sum()
umsatz_kategorie.plot(kind='bar', title='Umsatz pro Kategorie')
plt.xlabel('Kategorie')
plt.ylabel('Umsatz in Euro')
plt.tight_layout()
plt.show()

# Plot 2: Verkäufe pro Tag
verkaeufe_pro_tag = df.groupby('Datum')['Gesamtpreis'].sum()
verkaeufe_pro_tag.plot(kind='line', marker='o', title='Täglicher Umsatz')
plt.xlabel('Datum')
plt.ylabel('Umsatz in Euro')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 3: Häufigkeit der verkauften Produkte
produkt_anzahl = df.groupby('Produkt')['Anzahl'].sum()
produkt_anzahl.plot(kind='pie', autopct='%1.1f%%', title='Verkaufsverteilung nach Produkt')
plt.ylabel('')
plt.tight_layout()
plt.show()

# Als CSV speichern
df.to_csv('verkaeufe.csv', index=False)
print("\nCSV-Datei 'verkaeufe.csv' wurde gespeichert.")

# Gesamtumsatz berechnen
gesamtumsatz = df['Gesamtpreis'].sum()
print(f"\nGesamtumsatz: {gesamtumsatz:.2f} Euro")
