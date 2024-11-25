import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('T1_Kunden_Mitarbeiter.db')
cursor = conn.cursor()

# Tabelle erstellen, falls sie nicht existiert
cursor.execute('''
CREATE TABLE IF NOT EXISTS C_Mitarbeiter (
    id INTEGER PRIMARY KEY,
    vorname TEXT,
    nachname TEXT
)
''')

# Beispieldaten einfügen
cursor.execute("INSERT INTO C_Mitarbeiter (vorname, nachname) VALUES ('Max', 'Mustermann')")
cursor.execute("INSERT INTO C_Mitarbeiter (vorname, nachname) VALUES ('Anna', 'Schmidt')")
cursor.execute("INSERT INTO C_Mitarbeiter (vorname, nachname) VALUES ('Peter', 'Müller')")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()