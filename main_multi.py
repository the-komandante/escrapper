import requests
from bs4 import BeautifulSoup
import re
import json
import csv

# URL de la página web que deseas analizar
categoria = "mobiliario"
url = f'https://multiplast.com.uy/decoracion-mobiliario/mobiliario'

# Realiza la solicitud a la página web
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
response = requests.get(url, headers=headers)

# Analiza el contenido HTML de la página
soup = BeautifulSoup(response.content, 'html.parser')

# Encuentra todos los elementos de producto
productos = soup.find_all('div', class_='grp5')


# Encuentra todos los elementos de producto

# Lista para almacenar la información de los productos
lista_productos = []

# Iterar sobre cada producto y extraer la información deseada
for producto in productos:
    # Extraer el nombre del producto
    
    try:
        nombre = producto.find("a", class_="tit").text
        link = producto.find('a', class_='tit')["href"]

        # Extraer el precio del producto (ejemplo, si el precio está en un span con clase 'precio')
        moneda = producto.find('span', class_='sim').text
        precio = producto.find('span', class_='monto').text

        imagen = "https:" + producto.find_all('img')[1]["src"]
        # Agregar los datos a la lista de productos
        lista_productos.append({
                'nombre': nombre,
                'moneda': moneda,
                'precio': precio,
                'img': imagen,
                'link': link
            })
    except:
        pass

archivo_csv = f'productos_mobiliario.csv'

# Mostrar los productos extraídos
campos = ['nombre', 'moneda', 'precio', 'img', 'link']

# Escribir en el archivo CSV
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=campos)

    # Escribir la fila de encabezados
    writer.writeheader()

    # Escribir los datos
    for producto in lista_productos:
        writer.writerow(producto)

print(f"Archivo CSV '{archivo_csv}' creado exitosamente.")
