# 🗺️ Mapa de Fotos con Geolocalización

Una aplicación Python que extrae las coordenadas GPS de tus fotos y las muestra en un mapa interactivo usando Folium.

## ✨ Características

- 📸 Extrae automáticamente coordenadas GPS de metadatos EXIF
- 🗺️ Crea mapas interactivos con Folium
- 📍 Muestra marcadores con popups de las fotos
- 📊 Estadísticas de procesamiento
- 🖼️ Soporte para múltiples formatos de imagen (JPG, PNG, TIFF)
- 🎯 Interfaz visual mejorada con iconos de cámara

## 🚀 Instalación

### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona o descarga este repositorio**
   ```bash
   git clone <tu-repositorio>
   cd my_map_photo
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crea la carpeta para tus fotos**
   ```bash
   mkdir fotos
   ```

4. **Coloca tus fotos en la carpeta `fotos/`**
   - Asegúrate de que las fotos tengan datos GPS en sus metadatos EXIF
   - Formatos soportados: JPG, JPEG, PNG, TIFF, TIF

## 📖 Uso

### Uso básico

1. **Ejecuta la aplicación**
   ```bash
   python app.py
   ```

2. **Abre el mapa generado**
   - Se creará un archivo `visor.html`
   - Ábrelo en tu navegador web

### Uso avanzado

```python
from app import create_photo_map

# Crear mapa personalizado
mapa = create_photo_map(
    fotos_folder="mi_carpeta_fotos/",
    output_file="mi_mapa.html"
)
```

## 📁 Estructura del proyecto

```
my_map_photo/
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias de Python
├── README.md          # Este archivo
├── fotos/             # Carpeta con tus fotos (crear manualmente)
└── visor.html         # Mapa generado (se crea automáticamente)
```

## 🔧 Configuración

### Personalizar la ubicación del mapa

Edita la función `create_photo_map()` en `app.py`:

```python
# Cambiar ubicación inicial del mapa
mapa = folium.Map(
    location=[tu_latitud, tu_longitud],  # Coordenadas de tu región
    zoom_start=6
)
```

### Cambiar el estilo del mapa

```python
# Usar diferentes tiles
mapa = folium.Map(
    location=[23.6345, -102.5528],
    zoom_start=6,
    tiles='Stamen Terrain'  # O 'CartoDB positron', 'OpenStreetMap', etc.
)
```

## 📋 Requisitos de las fotos

Para que la aplicación funcione correctamente, tus fotos deben:

- ✅ Tener metadatos EXIF con datos GPS
- ✅ Estar en formato JPG, JPEG, PNG, TIFF o TIF
- ✅ Haber sido tomadas con un dispositivo que registre ubicación (smartphone, cámara con GPS)

### Verificar datos GPS en tus fotos

Puedes verificar si tus fotos tienen datos GPS usando herramientas como:
- **Windows**: Propiedades del archivo → Detalles
- **macOS**: Vista previa → Inspector → EXIF
- **Linux**: `exiftool nombre_foto.jpg`

## 🐛 Solución de problemas

### "No se encontraron fotos con datos GPS"
- Verifica que tus fotos tengan habilitado el GPS al tomarlas
- Algunas fotos editadas pueden perder los metadatos GPS

### "La carpeta 'fotos/' no existe"
- Crea la carpeta `fotos/` en el directorio del proyecto
- Coloca tus fotos dentro de esta carpeta

### Error de dependencias
- Asegúrate de tener Python 3.7+
- Ejecuta `pip install --upgrade pip` antes de instalar dependencias

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la aplicación:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Tu Nombre - [@tu_usuario](https://github.com/tu_usuario)

## 🙏 Agradecimientos

- [Folium](https://python-visualization.github.io/folium/) - Para la creación de mapas interactivos
- [Pillow (PIL)](https://pillow.readthedocs.io/) - Para el procesamiento de imágenes
- [OpenStreetMap](https://www.openstreetmap.org/) - Para los datos del mapa base
