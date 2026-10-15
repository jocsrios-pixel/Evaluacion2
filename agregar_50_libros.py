import random
import string
import requests

BASE_URL = "http://localhost:5000/api/v1/books"

NOMBRES = ["Carlos", "Ana", "Luis", "Maria", "Pedro", "Sofia", "Diego", "Valentina"]
APELLIDOS = ["Silva", "Rojas", "Morales", "Concha", "Gomez", "Torres", "Vargas", "Muñoz"]
TEMAS = ["Redes Avanzadas", "Python para DevNet", "Ciberseguridad", "Microservicios", "Cloud Computing"]

def generar_autor():
    return f"{random.choice(NOMBRES)}_{random.choice(APELLIDOS)}"

def generar_titulo(i):
    return f"{random.choice(TEMAS)} - Vol. {i}"

def generar_isbn():
    numeros = "".join(random.choices(string.digits, k=8))
    dv = random.choice("0123456789K")
    return f"{numeros}{dv}"

def agregar_libros(cantidad=50, id_inicio=8):
    print(f"=== Creando {cantidad} libros al azar ===")
    for i in range(cantidad):
        libro_id = id_inicio + i
        payload = {
            "id": libro_id,
            "title": generar_titulo(i + 1),
            "author": generar_autor(),
            "isbn": generar_isbn()
        }
        res = requests.post(BASE_URL, json=payload, headers={"Content-Type": "application/json"})
        if res.status_code in [200, 201]:
            print(f"[OK] Creado Libro ID {libro_id}: {payload['title']} - Autor: {payload['author']}")

def listar_todos():
    print("\n=== LISTADO COMPLETO DE LIBROS ===")
    res = requests.get(BASE_URL)
    if res.status_code == 200:
        libros = res.json()
        print(f"Total de libros registrados: {len(libros)}\n")
        print(f"{'ID':<5} | {'ISBN':<12} | {'AUTOR':<20} | {'TÍTULO'}")
        print("-" * 70)
        for lib in libros:
            print(f"{lib.get('id',''):<5} | {lib.get('isbn',''):<12} | {lib.get('author',''):<20} | {lib.get('title','')}")

if __name__ == "__main__":
    agregar_libros(50, id_inicio=8)
    listar_todos()