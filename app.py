import folium
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os

def get_gps_from_exif(img_path):
    img = Image.open(img_path)
    exif = img._getexif()
    if not exif:
        return None
    
    gps_info = {}
    for tag, value in exif.items():
        tag_name = TAGS.get(tag)
        if tag_name == "GPSInfo":
            for key in value:
                gps_info[GPSTAGS.get(key)] = value[key]

    if not gps_info:
        return None

    # Convertir a decimal

    
    
    def to_float(ratio):
        try:
            return ratio[0] / ratio[1]  # num/den
        except TypeError:
            return float(ratio)  # IFDRational

    def convert_to_degrees(value):
        d, m, s = value
        return to_float(d) + (to_float(m) / 60.0) + (to_float(s) / 3600.0)

    lat = convert_to_degrees(gps_info['GPSLatitude'])
    if gps_info['GPSLatitudeRef'] == 'S':
        lat = -lat
    lon = convert_to_degrees(gps_info['GPSLongitude'])
    if gps_info['GPSLongitudeRef'] == 'W':
        lon = -lon

    return lat, lon

# Crear mapa
mapa = folium.Map(location=[20, -100], zoom_start=5)

folder = "fotos/"
for foto in os.listdir(folder):
    path = os.path.join(folder, foto)
    coords = get_gps_from_exif(path)
    if coords:
        folium.Marker(
            location=coords,
            popup=f"<img src='{path}' width='200px'>"
        ).add_to(mapa)

mapa.save("visor.html")

