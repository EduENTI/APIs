#!/usr/bin/python3
import requests
import os

#Definimos el endpoint
API_URL = "https://api.fbi.gov/wanted/v1/list"
#Creamos un diccionario para los filtros
filtros_activos = {}

#Función para mandar la petición a la API y definimos por defecto los parámetros como ninguno
def make_request(params=None):
    
    #Definimos el user agent para evitar ser bloqueados
    headers = {'User-Agent': 'Mozilla/5.0'}
    #Guardamos la respuesta de la API
    response = requests.get(API_URL, params=params, headers=headers)
    #Devolvemos el contenido JSON de la respuesta
    return response.json()

#Función para aplicar los filtros seleccionados y obtener datos
def aplicar_filtros():

    return make_request(filtros_activos)

#Función para mostrar un listado simplificado al listar a 20
def mostrar_listado_simple(data):
    
    #Obtenemos los elementos de la respuesta o una lista vacía si no hay
    items = data.get("items", [])
    
    #Si no hay items, avisamos al usuario y salimos
    if not items:

        print("No se encontraron resultados.")
        input("Presiona Enter para continuar...")
        return
    #Si hay items, damos el total
    print(f"\nTotal de resultados: {data.get('total', len(items))}")
    
    #Y después listamos los 20 primeros items de la lista
    for i, item in enumerate(items[:20], start=1):
        print(f"{i}. {item.get('title')} (ID: {item.get('uid')})")

    input("\nPresiona Enter para continuar...")

#Función para listar todos los detalles al buscar por nombre
def mostrar_detallado(items):

    #Si no hay resultados imprimimos un mensaje y salimos
    if not items or not isinstance(items, list):
        
        print("No se encontraron resultados válidos.")
        return
    
    #Si hay varias fechas de nacimiento las juntamos y si no hay ninguna decimos que no está disponible
    for item in items:

        fechas_nacimiento = item.get('dates_of_birth_used')

        if isinstance(fechas_nacimiento, list):

            fechas_str = '; '.join(fechas_nacimiento)
        else:

            fechas_str = "No disponible"
        
        #Extraemos y printamos los detalles
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

#Función para el menú de aplicar filtros
def menu_filtros():
    
    #Bucle principal
    while True:
        #Limpiamos la pantalla para que quede bonito
        os.system('cls' if os.name == 'nt' else 'clear')
        #Printamos el menú
        print("\n=== FILTROS DISPONIBLES ===")
        print("1. Filtrar por sexo")
        print("2. Filtrar por raza")
        print("3. Filtrar por color de ojos")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")
        
        #Cogemos el input, lo transformamos en minúsculas y lo guardamos en el diccionario con una key en función de la opción escogida
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

#Función para limpiar los filtros establecidos
def limpiar_filtros():

    filtros_activos.clear()
    print("Filtros eliminados.")

#Función para buscar por nombre
def buscar_por_nombre():
    #Cogemos el nombre y lo pasamos a mayúsculas para comparar
    nombre_buscado = input("Introduce el nombre a buscar: ").strip().upper()
    data = make_request({"title": nombre_buscado})
    
    #Si no hay datos o resultados avisamos
    if not data or not data.get("items"):
        print("No se encontraron resultados.")
        input("Presiona Enter para continuar...")
        return

    items = data.get("items", [])

    #Búsqueda exacta por nombre
    resultados_exactos = [
        item for item in items
        if item.get("title", "").upper() == nombre_buscado
    ]
    
    #Si hay resultados exactos los mostramos y salimos
    if resultados_exactos:
        mostrar_detallado(resultados_exactos)
        return

    #Búsqueda parcial por palabras en orden (ayuda de la IA)
    palabras_buscadas = nombre_buscado.split()
    resultados_parciales = [
        item for item in items
        if all(palabra in item.get("title", "").upper() for palabra in palabras_buscadas)
    ]
    
    #Si hay resultados de la búsqueda parcial los mostramos, si no avisamos y salimos
    if resultados_parciales:
        mostrar_detallado(resultados_parciales)
    else:
        print("No se encontraron coincidencias.")
        input("Presiona Enter para continuar...")

#Función que define el menú principal del programa
def menu_principal():

    while True:
        #En función del sistema operativo limpiamos la pantalla para que sea bonito
        os.system('cls' if os.name == 'nt' else 'clear')
        #Mostramos el menú
        print("\n=== FBI MOST WANTED ===")
        print("1. Aplicar filtros")
        print("2. Limpiar filtros")
        print("3. Listar 20 más buscados (con filtros)")
        print("4. Buscar por nombre (detallado)")
        print("0. Salir")
        
        #Mostramos los filtros activos si hay y si no ponemos "Ninguno"
        print(f"\nFiltros activos: {filtros_activos if filtros_activos else 'Ninguno'}")

        opcion = input("Selecciona una opción: ")
        
        #En función de la opción seleccionada hacemos una u otra cosa
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

#Llamamos a la función principal para empezar el flujo de ejecución
menu_principal()
