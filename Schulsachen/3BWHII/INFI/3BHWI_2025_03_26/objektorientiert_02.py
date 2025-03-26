from objektorientiert_01 import VerkaufsAnalyse




# Objekt erstellen
analyse = VerkaufsAnalyse("verkaeufe_50.csv")

# Methoden aufrufen
analyse.laden()
analyse.berechne_gesamtpreis()
analyse.zeige_uebersicht()
print(analyse.umsatz_pro_kategorie())
analyse.plot_umsatz_pro_tag()
analyse.speichern("verkaeufe_neu.csv")
