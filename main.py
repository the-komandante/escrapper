import requests
from bs4 import BeautifulSoup
import re
import json
import csv

# URL de la página web que deseas analizar
categoria = "iluminacion"
url = f'https://multiplast.com.uy/{categoria}'

# Realiza la solicitud a la página web
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
response = requests.get(url, headers=headers)

# Analiza el contenido HTML de la página
soup = BeautifulSoup(response.content, 'html.parser')

# Encuentra todos los elementos de producto
productos = soup.find_all('div', class_='item-box')

# Expresión regular para capturar los objetos de producto
pattern = r"var ga4_product_impression_\d+\s*=\s*({[\s\S]*?});[\s\S]*?'currency':\s*'(\w+)'"

# Lista para almacenar la información de todos los productos
lista_productos = []

# Itera sobre los productos encontrados
for producto in productos:
    # Extrae el string de JavaScript del script del producto
    script_content = producto.script.string
    
    if script_content:
        # Encuentra el objeto de producto usando la expresión regular
        # La expresión regular ahora captura también la moneda
        matches = re.findall(pattern, script_content)
        
        for match in matches:
            # El primer grupo es el JSON del producto, el segundo es la moneda
            cleaned_match = match[0].replace("\r\n", "").replace("'", '"')
            currency = match[1]
            
            # Convierte la cadena JSON en un diccionario de Python
            producto_info = json.loads(cleaned_match)
            
            # Añade la moneda al diccionario de información del producto
            producto_info['currency'] = currency
            
            # Añade el diccionario a la lista de productos
            lista_productos.append(producto_info)

# Muestra los productos extraídos
for producto in lista_productos:
    print(f"Título: {producto['item_name']}")
    print(f"ID del Producto: {producto['item_id']}")
    print(f"Precio: {producto['price']}")
    print(f"Categoría: {producto['item_category']}")
    print(f"Moneda: {producto['currency']}")
    print('--------------------')



# Nombre del archivo CSV que deseas crear
archivo_csv = f'productos_{categoria}.csv'

# Campos que deseas incluir en el CSV

# Escribir en el archivo CSV
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=lista_productos[0].keys())

    # Escribir la fila de encabezados
    writer.writeheader()

    # Escribir los datos
    for producto in lista_productos:
        writer.writerow(producto)

print(f"Archivo CSV '{archivo_csv}' creado exitosamente.")
