import pandas as pd
import matplotlib.pyplot as plt

class VerkaufsAnalyse:
    def __init__(self, dateipfad):
        self.dateipfad = dateipfad
        self.df = None

    def laden(self):
        self.df = pd.read_csv(self.dateipfad)
        self.df['Datum'] = pd.to_datetime(self.df['Datum'])
        print("Datei geladen und Datum konvertiert.")

    def zeige_uebersicht(self):
        print(self.df.head())
        print("\nSpalten:", self.df.columns.tolist())

    def berechne_gesamtpreis(self):
        self.df['Gesamtpreis'] = self.df['Preis'] * self.df['Anzahl']

    def umsatz_pro_kategorie(self):
        return self.df.groupby('Kategorie')['Gesamtpreis'].sum()

    def plot_umsatz_pro_tag(self):
        tagesumsatz = self.df.groupby('Datum')['Gesamtpreis'].sum()
        tagesumsatz.plot(title='Umsatz pro Tag', marker='o')
        plt.ylabel('Euro')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def speichern(self, pfad_neu):
        self.df.to_csv(pfad_neu, index=False)
        print(f"Gespeichert als: {pfad_neu}")

# Objekt erstellen
analyse = VerkaufsAnalyse("verkaeufe_50.csv")

# Methoden aufrufen
analyse.laden()
analyse.berechne_gesamtpreis()
analyse.zeige_uebersicht()
print(analyse.umsatz_pro_kategorie())
analyse.plot_umsatz_pro_tag()
analyse.speichern("verkaeufe_neu.csv")