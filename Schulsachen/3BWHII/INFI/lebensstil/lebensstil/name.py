import argparse

def main():
    parser = argparse.ArgumentParser(description="Gibt Vor- und Nachnamen sowie optionale Informationen aus.")
    
    # Pflichtargumente
    parser.add_argument("vorname", help="Der Vorname der Person")
    parser.add_argument("nachname", help="Der Nachname der Person")

    # Optionale Argumente
    parser.add_argument("--anrede", help="Anrede der Person (z. B. Herr oder Frau)", default="")
    parser.add_argument("--alter", type=int, help="Alter der Person", default=None)

    args = parser.parse_args()

    # Ausgabe
    if args.anrede:
        print(f"Anrede: {args.anrede}")
    print(f"Vorname: {args.vorname}")
    print(f"Nachname: {args.nachname}")
    if args.alter is not None:
        print(f"Alter: {args.alter}")

if __name__ == "__main__":
    main()

