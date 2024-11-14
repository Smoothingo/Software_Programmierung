import pandas as pd
import sqlite3

# Pfad zur SQLite-Datenbank
sqlite_db = r'Schulsachen\3BWHII\INFI\A3\T1_Kunden_Mitarbeiter.db'
conn = sqlite3.connect(sqlite_db)

# Erstellt eine Verbindung zur SQLite-Datenbank
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
mytables = cur.fetchall()

# Ausgabe der Tabellen und der ersten 5 Zeilen jeder Tabelle
for row in mytables:
    print('''*********************************************\n
--      <<<<<<{row}>>>>>>\n
-----------------------------------------------'''.format(row=row[0]))
    cur.execute("SELECT * FROM {retrieved_table};".format(retrieved_table=row[0]))
    table_data = cur.fetchmany(5)
    for detailrow in table_data:
        print(detailrow)
    print('*********************************************')

# Beispielabfrage und Ausgabe
cur.execute("SELECT ID, Nachname FROM C_Kunden;")
result = cur.fetchall()
for row in result:
    print(row)



# SQL-Abfrage zur Berechnung der Anzahl der Kunden je Kundenbetreuer
query = """
SELECT m.ID, m.Vorname, m.Nachname, COUNT(k.ID) as Anzahl_Kunden
FROM C_Mitarbeiter m
JOIN C_Kunden k ON k.[Kunden-Betreuer] = m.ID
GROUP BY m.ID, m.Vorname, m.Nachname;
"""

# Erstellen eines DataFrames aus der SQL-Abfrage
my_df = pd.read_sql(query, conn)

# Sortieren des DataFrames nach der Anzahl der Kunden (absteigend)
my_df_sorted = my_df.sort_values(by='Anzahl_Kunden', ascending=False)

# Ausgabe der Top 5 Kundenbetreuer im Terminal
print("Top 5 Kundenbetreuer nach Anzahl der Kunden:")
print(my_df_sorted.head())

# Optional: Speichern des sortierten DataFrames als HTML-Datei
my_df_sorted.to_html('df_sorted.html')

# Schließen der Datenbankverbindung
conn.close()