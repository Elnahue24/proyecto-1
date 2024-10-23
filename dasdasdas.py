import requests
from bs4 import BeautifulSoup
import json

# URL de búsqueda de propiedades en Montevideo en Mercado Libre
url = 'https://inmuebles.mercadolibre.com.uy/casas/venta/montevideo/'

# Función para obtener y parsear el contenido HTML de una página
def obtener_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Error al obtener el contenido de la página: {response.status_code}")
            return None
    except Exception as e:
        print(f"Excepción al realizar la solicitud: {e}")
        return None

# Función para extraer los datos de las propiedades
def extraer_datos_propiedades(html):
    propiedades = []
    
    # Encuentra el contenedor principal de las propiedades
    lista_propiedades = html.find_all('li', class_='ui-search-layout__item')  # Modificar si cambia la estructura
    
    for propiedad in lista_propiedades[:10]:  # Limitar a 10 propiedades
        try:
            precio = propiedad.find('span', class_='price-tag-fraction').get_text().strip().replace(',', '')
            tamano = propiedad.find('li', class_='ui-search-card-attributes_attribute').get_text().strip().replace(' m²', '') if propiedad.find('li', class='ui-search-card-attributes__attribute') else None
            habitaciones = propiedad.find_all('li', class_='ui-search-card-attributes_attribute')[1].get_text().strip() if len(propiedad.find_all('li', class='ui-search-card-attributes__attribute')) > 1 else None
            link = propiedad.find('a', class_='ui-search-link')['href']
            
            propiedades.append({
                "precio": float(precio) if precio else None,
                "tamano": int(tamano) if tamano else None,
                "habitaciones": int(habitaciones) if habitaciones else None,
                "link": link
            })
        except Exception as e:
            print(f"Error al extraer datos de una propiedad: {e}")
            continue
    
    return propiedades

# Obtener el contenido HTML de la página
html = obtener_html(url)

# Extraer los datos de las propiedades si el HTML fue cargado correctamente
if html:
    datos_propiedades = extraer_datos_propiedades(html)

    # Guardar los datos en un archivo JSON
    with open('propiedades_montevideo_mercadolibre.json', 'w') as f:
        json.dump({"propiedades": datos_propiedades}, f, indent=4)

    print("Datos guardados en propiedades_montevideo_mercadolibre.json")