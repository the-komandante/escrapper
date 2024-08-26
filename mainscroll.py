from seleniumwire import webdriver  # Importa webdriver desde selenium-wire
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv
import re
import json

# Configura Selenium para utilizar Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Opcional: para ejecutar sin abrir una ventana del navegador
driver = webdriver.Chrome(options=options)

# URL de la página que quieres scrapear
categoria = "iluminacion"
url = f'https://multiplast.com.uy/{categoria}'

# Abre la página
driver.get(url)

# Scrollea hacia abajo para cargar más contenido
scroll_pause_time = 2  # Tiempo de espera entre cada scroll

# Scroll hasta el final de la página varias veces
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scrollea hacia abajo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Espera para que el contenido se cargue
    time.sleep(scroll_pause_time)

    # Captura los requests realizados
    comment = """for request in driver.requests:
        if request.response:
            print(f"URL: {request.url}")
            print(f"Status Code: {request.response.status_code}")
            print(f"Content Type: {request.response.headers['Content-Type']}")
            # Aquí puedes analizar o guardar la respuesta del request"""

    # Verifica si se cargó nuevo contenido
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # Si la altura no cambia, hemos llegado al final de la página
    last_height = new_height

# Obtén el HTML final de la página
html = driver.page_source   
with open("output.html", "w", encoding="utf8") as text_file:
    text_file.write(html)

# Analiza el HTML con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

productos = soup.find_all('div', class_='it grp4')

lista_productos = []

# Iterar sobre cada producto y extraer la información deseada
for producto in productos:
    # Extraer el nombre del producto
    
    try:
        nombre = producto.find("a", class_="tit").text
        link = producto.find('a', class_='tit')["href"]

        # Extraer el precio del producto (ejemplo, si el precio está en un span con clase 'precio')
        moneda = producto.find('span', class_='sim').text
        precio = producto.find('span', class_='monto').text.replace(".", "")

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

archivo_csv = f'productos_{categoria}.csv'

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
