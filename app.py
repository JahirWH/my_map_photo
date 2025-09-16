#!/usr/bin/env python3
"""
Mapa de Fotos con Geolocalización
=================================

Esta aplicación extrae las coordenadas GPS de las fotos en la carpeta 'fotos/'
y las muestra en un mapa interactivo usando Folium.

Autor: JahirWH
Fecha: 2025
"""

import folium
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import sys
from pathlib import Path    
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_gps_from_exif(img_path):
    """
    Extrae las coordenadas GPS de los metadatos EXIF de una imagen.
    
    Args:
        img_path (str): Ruta a la imagen
        
    Returns:
        tuple: (latitud, longitud) en grados decimales, o None si no se encuentran datos GPS
    """
    try:
        img = Image.open(img_path)
        exif = img._getexif()
        
        if not exif:
            logger.warning(f"No se encontraron metadatos EXIF en {img_path}")
            return None
        
        gps_info = {}
        for tag, value in exif.items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for key in value:
                    gps_info[GPSTAGS.get(key)] = value[key]

        if not gps_info:
            logger.warning(f"No se encontraron datos GPS en {img_path}")
            return None

        # Verificar que tenemos los datos necesarios
        required_keys = ['GPSLatitude', 'GPSLatitudeRef', 'GPSLongitude', 'GPSLongitudeRef']
        if not all(key in gps_info for key in required_keys):
            logger.warning(f"Datos GPS incompletos en {img_path}")
            return None

        def to_float(ratio):
            """Convierte una fracción a float."""
            try:
                return ratio[0] / ratio[1]  # num/den
            except (TypeError, ZeroDivisionError):
                return float(ratio)  # IFDRational

        def convert_to_degrees(value):
            """Convierte coordenadas DMS (Grados, Minutos, Segundos) a grados decimales."""
            d, m, s = value
            return to_float(d) + (to_float(m) / 60.0) + (to_float(s) / 3600.0)

        # Convertir latitud
        lat = convert_to_degrees(gps_info['GPSLatitude'])
        if gps_info['GPSLatitudeRef'] == 'S':
            lat = -lat
            
        # Convertir longitud
        lon = convert_to_degrees(gps_info['GPSLongitude'])
        if gps_info['GPSLongitudeRef'] == 'W':
            lon = -lon

        logger.info(f"Coordenadas extraídas de {img_path}: ({lat:.6f}, {lon:.6f})")
        return lat, lon
        
    except Exception as e:
        logger.error(f"Error procesando {img_path}: {str(e)}")
        return None

def create_photo_map(fotos_folder="fotos/", output_file="visor.html"):
    """
    Crea un mapa interactivo con las fotos que contienen datos GPS.
    
    Args:
        fotos_folder (str): Carpeta que contiene las fotos
        output_file (str): Archivo HTML de salida
        
    Returns:
        folium.Map: Mapa creado
    """
    # Verificar que la carpeta existe
    if not os.path.exists(fotos_folder):
        logger.error(f"La carpeta '{fotos_folder}' no existe")
        return None
    
    # Crear mapa centrado en México
    mapa = folium.Map(
        location=[23.6345, -102.5528],  # Centro de México
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Contadores para estadísticas
    fotos_procesadas = 0
    fotos_con_gps = 0
    fotos_sin_gps = 0
    
    # Procesar cada foto en la carpeta
    for foto in os.listdir(fotos_folder):
        # Solo procesar archivos de imagen
        if not foto.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.tif')):
            continue
            
        path = os.path.join(fotos_folder, foto)
        fotos_procesadas += 1
        
        coords = get_gps_from_exif(path)
        if coords:
            lat, lon = coords
            fotos_con_gps += 1
            
            # Crear popup con la imagen
            popup_html = f"""
            <div style="text-align: center;">
                <h4>{foto}</h4>
                <img src='{path}' width='300px' style='max-height: 300px; object-fit: contain;'>
                <p><strong>Coordenadas:</strong><br>
                Lat: {lat:.6f}<br>
                Lon: {lon:.6f}</p>
            </div>
            """
            
            # Agregar marcador al mapa
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_html, max_width=400),
                tooltip=foto,
                icon=folium.Icon(color='red', icon='camera')
            ).add_to(mapa)
        else:
            fotos_sin_gps += 1
    
    # Mostrar estadísticas
    logger.info(f"Procesadas {fotos_procesadas} fotos")
    logger.info(f"Fotos con GPS: {fotos_con_gps}")
    logger.info(f"Fotos sin GPS: {fotos_sin_gps}")
    
    if fotos_con_gps == 0:
        logger.warning("No se encontraron fotos con datos GPS")
        return mapa
    
    # Guardar mapa
    mapa.save(output_file)
    logger.info(f"Mapa guardado en {output_file}")
    
    return mapa

def main():
    """Función principal."""
    print("🗺️  Generador de Mapa de Fotos con Geolocalización")
    print("=" * 50)
    
    # Verificar que existe la carpeta de fotos
    fotos_folder = "fotos/"
    if not os.path.exists(fotos_folder):
        print(f"❌ Error: La carpeta '{fotos_folder}' no existe")
        print("   Crea la carpeta y coloca tus fotos allí")
        sys.exit(1)
    
    # Crear el mapa
    mapa = create_photo_map()
    
    if mapa:
        print("✅ Mapa generado exitosamente!")
        print(f"   Abre 'visor.html' en tu navegador para ver el resultado")
    else:
        print("❌ Error al generar el mapa")
        sys.exit(1)

if __name__ == "__main__":
    main()

