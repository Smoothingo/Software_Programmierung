import folium

# Definiere die Koordinaten für die Karte
location = [48.321717, 16.207151]

# Erstelle die Karte mit der angegebenen Position
m = folium.Map(
    location=location,
    zoom_start=2,  # Standard-Zoomstufe
    max_bounds=True
)

# Füge einen Marker an der angegebenen Position hinzu
folium.Marker(location, tooltip="Location").add_to(m)

# Speichere die Karte in einer HTML-Datei
m.save('map.html')