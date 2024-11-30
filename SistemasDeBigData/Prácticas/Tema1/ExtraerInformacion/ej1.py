import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

url = "https://www.20minutos.es/ultimas-noticias/"

# Función para obtener el HTML de una URL
def obtener_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print("Error al acceder al sitio:", response.status_code)
        return None

# Función para extraer contenido del artículo
def extraer_contenido(url):
    soup = obtener_html(url)
    if soup:
        content_tag = soup.find('div', class_='article-text')  # Clase que contiene el contenido
        if content_tag:
            return content_tag.get_text(strip=True, separator=" ")  # Extraer contenido y unir con espacios
    return "Contenido no encontrado"

# Función para extraer datos de la página principal
def extraer_datos(soup):
    # Buscamos los artículos en la clase 'media' que contiene cada artículo
    articles = soup.find_all('article', class_='media')
    data = []

    for article in articles:
        # El título se encuentra en el h1 dentro de un a
        title_tag = article.find('h1').find('a') if article.find('h1') else None
        title = title_tag.get_text(strip=True) if title_tag else "Título no encontrado"

        # El enlace se obtiene del atributo href del a
        link = title_tag['href'] if title_tag else "Enlace no encontrado"
        if not link.startswith('http'):
            link = 'https://www.20minutos.es' + link  # Asegurar que el enlace sea completo

        # Extraer el contenido del artículo
        content = extraer_contenido(link)

        data.append({"Título": title, "Enlace": link, "Contenido": content})

    return data

# Guardar datos en un DataFrame
def guardar_datos(data, archivo_csv):
    df = pd.DataFrame(data)
    df.to_csv(archivo_csv, index=False)
    print(f"Datos guardados en {archivo_csv}")
    return df

# Análisis de frecuencia de palabras
def analizar_frecuencia_palabras(df):
    all_titles = " ".join(df["Título"])
    word_count = Counter(all_titles.split())
    print("Palabras más comunes en los títulos:")
    for word, count in word_count.most_common(10):
        print(f"{word}: {count}")

# Paso 5: Visualización
def graficar_longitud_contenidos(df):
    df['Longitud_Contenido'] = df['Contenido'].apply(len)
    plt.hist(df['Longitud_Contenido'], bins=10, color='skyblue', edgecolor='black')
    plt.title("Distribución de la longitud de los contenidos")
    plt.xlabel("Longitud")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

# Función principal
def main():
    # Obtener el HTML del sitio
    soup = obtener_html(url)
    if not soup:
        return

    # Extraer datos
    data = extraer_datos(soup)

    # Guardar datos en un archivo CSV
    archivo_csv = "articulos_20minutos.csv"
    df = guardar_datos(data, archivo_csv)

    # Análisis de palabras
    analizar_frecuencia_palabras(df)

    # Visualización
    graficar_longitud_contenidos(df)

# Ejecutar el script
if __name__ == "__main__":
    main()
