#!/usr/bin/python3
import requests
import os

API_URL = "https://api.fbi.gov/wanted/v1/list"
filtros_activos = {}

def make_request(params=None):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la API del FBI: {e}")
        return None

def aplicar_filtros():
    return make_request(filtros_activos)

def mostrar_listado_simple(data):
    items = data.get("items", [])

    if not items:
        print("No se encontraron resultados.")
        input("Presiona Enter para continuar...")
        return

    print(f"\nTotal de resultados: {data.get('total', len(items))}")
    for i, item in enumerate(items[:20], start=1):
        print(f"{i}. {item.get('title')} (ID: {item.get('uid')})")

    input("\nPresiona Enter para continuar...")

def mostrar_detallado(items):
    if not items or not isinstance(items, list):
        print("No se encontraron resultados válidos.")
        return

    for item in items:
        fechas_nacimiento = item.get('dates_of_birth_used')
        if isinstance(fechas_nacimiento, list):
            fechas_str = ', '.join(fechas_nacimiento)
        else:
            fechas_str = "No disponible"

        print(f"\nNombre: {item.get('title')}")
        print(f"Descripción: {item.get('description')}")
        print(f"Sexo: {item.get('sex')}")
        print(f"Raza: {item.get('race')}")
        print(f"Ojos: {item.get('eyes')}")
        print(f"Fecha de nacimiento: {fechas_str}")
        print(f"Edad: {item.get('age_range')}")
        print(f"Altura: {item.get('height_min')} - {item.get('height_max')} pulgadas")
        print(f"Peso: {item.get('weight')}")
        print(f"Advertencia: {item.get('warning_message')}")
        print(f"Recompensa: {item.get('reward_text')}")
        print(f"Más información: {item.get('url')}")
        print("-" * 50)

    input("\nPresiona Enter para continuar...")

def menu_filtros():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== FILTROS DISPONIBLES ===")
        print("1. Filtrar por sexo")
        print("2. Filtrar por raza")
        print("3. Filtrar por color de ojos")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            sexo = input("Introduce sexo (male/female): ").lower()
            filtros_activos["sex"] = sexo
        elif opcion == "2":
            raza = input("Introduce raza (black/white/asian): ").lower()
            filtros_activos["race"] = raza
        elif opcion == "3":
            ojos = input("Introduce color de ojos (brown/blue/green): ").lower()
            filtros_activos["eyes"] = ojos
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def limpiar_filtros():
    filtros_activos.clear()
    print("Filtros eliminados.")

def buscar_por_nombre():
    nombre = input("Introduce el nombre a buscar: ").strip()
    data = make_request({"title": nombre})
    if data:
        mostrar_detallado(data.get("items", []))

def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== FBI MOST WANTED ===")
        print("1. Aplicar filtros")
        print("2. Limpiar filtros")
        print("3. Listar 20 más buscados (con filtros)")
        print("4. Buscar por nombre (detallado)")
        print("0. Salir")

        print(f"\nFiltros activos: {filtros_activos if filtros_activos else 'Ninguno'}")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_filtros()
        elif opcion == "2":
            limpiar_filtros()
        elif opcion == "3":
            data = aplicar_filtros()
            if data:
                mostrar_listado_simple(data)
        elif opcion == "4":
            buscar_por_nombre()
        elif opcion == "0":
            print("\nSaliendo del programa...")
            break
        else:
            print("Opción inválida.")

menu_principal()
