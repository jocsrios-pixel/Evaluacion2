import sys
import urllib.parse
import requests

GRAPH_URL = "https://graphhopper.com/api/1/route?"
# Tu clave real de GraphHopper
KEY = "e0ca60ec-c547-4d41-9483-bd7aa5da000b"


def geocodificar(ubicacion, key):
    """Obtiene latitud y longitud de una ubicación usando GraphHopper."""
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    query_params = {
        "q": ubicacion,
        "limit": "1",
        "key": key,
        "locale": "es"
    }
    url = geocode_url + urllib.parse.urlencode(query_params)
    
    try:
        res = requests.get(url)
        data = res.json()
        if res.status_code == 200 and len(data.get("hits", [])) > 0:
            point = data["hits"][0]["point"]
            nombre = data["hits"][0].get("name", ubicacion)
            pais = data["hits"][0].get("country", "")
            return point["lat"], point["lng"], f"{nombre}, {pais}".strip(", ")
        else:
            print(f"Error: No se encontró la ubicación '{ubicacion}'.")
            return None, None, None
    except Exception as e:
        print(f"Error de conexión en geocodificación: {e}")
        return None, None, None


def obtener_ruta(lat_orig, lng_orig, lat_dest, lng_dest, vehiculo, key):
    """Obtiene la ruta e instrucciones paso a paso."""
    params = [
        ("point", f"{lat_orig},{lng_orig}"),
        ("point", f"{lat_dest},{lng_dest}"),
        ("vehicle", vehiculo),
        ("locale", "es"),
        ("instructions", "true"),
        ("key", key)
    ]
    url = GRAPH_URL + urllib.parse.urlencode(params)
    return requests.get(url)


def main():
    print("=" * 65)
    print("      SISTEMA DE GEOLOCALIZACIÓN Y RUTAS - API LTDA.")
    print("            Planificador de Viajes a la Biblioteca")
    print("=" * 65)

    while True:
        print("\nIngrese punto de origen y destino.")
        print("Para salir en cualquier momento, escriba 's' o 'salir'.\n")

        origen_input = input("Ubicación de Origen: ").strip()
        if origen_input.lower() in ["s", "salir"]:
            print("Saliendo del programa. ¡Hasta pronto!")
            sys.exit(0)

        destino_input = input("Ubicación de Destino: ").strip()
        if destino_input.lower() in ["s", "salir"]:
            print("Saliendo del programa. ¡Hasta pronto!")
            sys.exit(0)

        print("\nSeleccione el medio de transporte:")
        print("1. Auto (car)")
        print("2. Bicicleta (bike)")
        print("3. A pie (foot)")
        
        opc = input("Opción (1-3) [Por defecto: 1]: ").strip()
        if opc.lower() in ["s", "salir"]:
            print("Saliendo del programa. ¡Hasta pronto!")
            sys.exit(0)

        perfiles = {"1": "car", "2": "bike", "3": "foot"}
        vehiculo = perfiles.get(opc, "car")

        print("\nCalculando coordenadas...")
        lat_o, lng_o, nom_o = geocodificar(origen_input, KEY)
        lat_d, lng_d, nom_d = geocodificar(destino_input, KEY)

        if not lat_o or not lat_d:
            print("No se pudo obtener las coordenadas. Intente nuevamente.")
            continue

        print(f"\nOrigen verificado:  {nom_o}")
        print(f"Destino verificado: {nom_d}")

        print("\nConsultando la ruta óptima...")
        res = obtener_ruta(lat_o, lng_o, lat_d, lng_d, vehiculo, KEY)

        if res.status_code == 200:
            datos = res.json()["paths"][0]
            dist_km = datos["distance"] / 1000.0
            tiempo_min = (datos["time"] / 1000.0) / 60.0

            print("\n" + "=" * 50)
            print("RESUMEN DEL VIAJE")
            print("=" * 50)
            print(f"Distancia total : {dist_km:.2f} km")
            print(f"Tiempo estimado : {tiempo_min:.2f} minutos")
            print("=" * 50)

            print("\nINSTRUCCIONES PASO A PASO (NARRATIVA DEL VIAJE):")
            print("-" * 50)
            instrucciones = datos.get("instructions", [])
            for idx, inst in enumerate(instrucciones, 1):
                d = inst.get("distance", 0) / 1000.0
                print(f"{idx:2d}. {inst.get('text', '')} ({d:.2f} km)")
            print("-" * 50)
        else:
            print(f"Error al obtener la ruta. Código HTTP: {res.status_code}")

        repetir = input("\n¿Desea consultar otra ruta? (Presione ENTER para continuar / 's' para salir): ").strip()
        if repetir.lower() in ["s", "salir"]:
            print("Gracias por utilizar el servicio. ¡Buen viaje!")
            break


if __name__ == "__main__":
    main()