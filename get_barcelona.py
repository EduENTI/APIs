#Importamos las librerías necesarias
import urllib.request, json, os

#Función para limpiar la pantalla uso un oneliner para decidir el comando en función del sistema operativo
def limpiar_pantalla():
    os.system('cls') if os.name == 'nt' else os.system('clear')

#Título de la app
title = "APP DEL TIEMPO"

#Función para imprimir el menú
def imprimir_menu():
    print("-" * len(title))
    print(title)
    print("-" * len(title))

#Diccionario con las ciudades
ciudades = {
            "Barcelona": (41.38879, 2.15899),
            "Badalona": (41.44699, 2.24503),
            "Zamora": (41.50333, -5.74456),
            "Madrid": (40.4165, -3.70256),
            "León": (42.60003, -5.57032)
        }

#Cojo las keys del diccionario (las ciudades) y las meto en una lista para poder iterar sobre los nombres
listaCiudades = list(ciudades.keys())

#Empieza el bucle principal
while True:
    limpiar_pantalla()

    imprimir_menu()

    print("Selecciona una ciudad:")
    
    #Índice para imprimir la lista
    numeroIndice = 1
    
    #Uso f"" para poder meter variables a mi gusto dentro de print
    for ciudad in ciudades:
        print(f"{numeroIndice}. {ciudad}")
        numeroIndice += 1

    
    print("0. Salir")
    opcion = int(input("Introduce el número de la ciudad: "))
    
    #Si el usuario elige 0 salimos del programa
    if opcion == 0:
        break
    #Si el usuario escoge una opción válida ejecutamos el flujo normal
    elif opcion >= 1 and opcion <= 5:

        limpiar_pantalla()

        imprimir_menu()
        
        #Como ahora es una lista va de 0 a n-1 por lo que transformamos el input del usuario
        ciudadElegida = listaCiudades[opcion - 1]

        lat, lon = ciudades[ciudadElegida]
    
        #Contruimos la URL, lo hago con f"" para poder separarla en líneas y que sea más legible y/o modificable
        url_tiempo = (
                        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation"
        f"&daily=temperature_2m_min,temperature_2m_max,precipitation_sum"
        f"&timezone=auto"            )

        #Parseamos los datos que nos llegan de la API
        with urllib.request.urlopen(url_tiempo) as datos:
	        parseado = json.load(datos)
        
        #Imprimimos lo que verá el usuario
        print(f"\nDatos actuales en {ciudadElegida}:")
        print(f"Temperatura: {parseado['current']['temperature_2m']} °C")
        print(f"Temperatura aparente: {parseado['current']['apparent_temperature']} °C")
        print(f"Humedad relativa: {parseado['current']['relative_humidity_2m']} %")
        print(f"Precipitación actual: {parseado['current']['precipitation']} mm\n")

        print(f"\nPredicción diaria en {ciudadElegida} a dia {parseado['daily']['time'][0]}:")
        print(f"Temperatura mínima: {parseado['daily']['temperature_2m_min'][0]}°C")
        print(f"Temperatura máxima: {parseado['daily']['temperature_2m_max'][0]}°C")
        print(f"Precipitación total: {parseado['daily']['precipitation_sum'][0]} mm\n")
    #Si no escoge una opción válida se lo diremos y volveremos arriba del bucle
    else:
        print("La opcion escogida no es válida!")

    #Un botón para continuar las interacciones del usuario con la app o quedar parados
    input("Presiona Enter para continuar...")
