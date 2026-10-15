# Evaluación N°2 - API Ltda. & Biblioteca Nacional

**Integrante:** Jocsan Rios  
**RUT:** 219752687  

## Descripción del Proyecto
Este repositorio contiene la solución completa para la modernización de los sistemas de la Biblioteca Nacional desarrollada por API Ltda.:

1. **API REST de Libros (`api_biblioteca.py` & `agregar_50_libros.py`):**
   - Servidor web Flask con endpoints para consultar, agregar y modificar el inventario de libros (`GET`, `POST`, `PUT`).
   - Script de automatización en Python para el ingreso masivo de 50 libros e impresión del catálogo completo.

2. **Software de Geolocalización (`geolocalizacion_graphhopper.py`):**
   - Integración con la API REST de GraphHopper.
   - Cálculo de rutas, distancias (km) y tiempos estimados (min) formateados a 2 decimales.
   - Interfaz en español con navegación narrada paso a paso y opción de salida rápida (`s`/`salir`).

## Requisitos de Instalación
- Python 3.x
- Flask (`pip install flask`)
- Requests (`pip install requests`)

## Instrucciones de Ejecución

### 1. Iniciar la API REST de la Biblioteca
```bash
python3 api_biblioteca.py