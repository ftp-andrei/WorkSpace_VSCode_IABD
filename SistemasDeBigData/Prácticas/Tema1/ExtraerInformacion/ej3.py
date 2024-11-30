import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Función para cargar y preparar los datos
def preparar_datos(archivo_csv):
    df = pd.read_csv(archivo_csv)
    
    # Verificar que exista la columna 'Título'
    if 'Título' not in df.columns:
        raise ValueError("El archivo CSV debe contener una columna llamada 'Título'.")
    
    # Calcular la longitud de los títulos
    df['Longitud_Titulo'] = df['Título'].apply(len)
    
    # Eliminar filas con valores nulos en 'Título'
    df = df.dropna(subset=['Título'])
    return df

# Gráfico: Distribución de temas
def distribucion_temas(df):
    # Clasificación básica por palabras clave en el título
    df['Categoria'] = df['Título'].apply(lambda x: "Deportes" if "fútbol" in x.lower() else 
                                         ("Política" if "Ayuso" in x.lower() else "Otros"))
    conteo_categorias = df['Categoria'].value_counts()
    conteo_categorias.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Distribución de Temas en los Artículos")
    plt.xlabel("Categorías")
    plt.ylabel("Número de Artículos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Gráfico: Evolución de la longitud promedio de los títulos
def evolucion_longitud_titulos(df):
    # Graficar la longitud promedio de los títulos
    longitud_promedio = df['Longitud_Titulo'].mean()
    plt.axhline(longitud_promedio, color='blue', linestyle='--', label=f'Longitud Promedio: {longitud_promedio:.2f}')
    plt.title("Evolución de la Longitud Promedio de los Títulos")
    plt.ylabel("Longitud Promedio")
    plt.xlabel("Artículos")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Gráfico: Frecuencia de palabras clave
def frecuencia_palabras_clave(df):
    all_titles = " ".join(df['Título'])
    word_count = Counter(all_titles.split())
    common_words = word_count.most_common(10)
    words, counts = zip(*common_words)
    
    plt.bar(words, counts, color='orange', edgecolor='black')
    plt.title("Palabras Más Comunes en los Títulos")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Mapa de calor: Relación entre temas y palabras clave
def mapa_calor_temas_palabras(df):
    # Clasificación básica por palabras clave en el título
    df['Categoria'] = df['Título'].apply(lambda x: "Deportes" if "fútbol" in x.lower() else 
                                         ("Política" if "Ayuso" in x.lower() else "Otros"))
    
    # Extraer palabras clave por categoría
    categoria_palabras = df.groupby('Categoria')['Título'].apply(lambda x: " ".join(x)).reset_index()
    categoria_palabras['Palabras'] = categoria_palabras['Título'].apply(lambda x: Counter(x.split()))
    
    # Crear una matriz de palabras clave
    palabras_clave = list(set(word for row in categoria_palabras['Palabras'] for word in row))
    matriz = pd.DataFrame(0, index=categoria_palabras['Categoria'], columns=palabras_clave)
    
    for _, row in categoria_palabras.iterrows():
        for palabra, count in row['Palabras'].items():
            if palabra in matriz.columns:
                matriz.loc[row['Categoria'], palabra] = count
    
    # Reducir palabras clave para una visualización legible (e.g., las 20 más comunes)
    palabras_comunes = matriz.sum(axis=0).sort_values(ascending=False).head(20).index
    matriz_reducida = matriz[palabras_comunes]
    
    # Visualizar mapa de calor
    plt.figure(figsize=(12, 8))
    sns.heatmap(matriz_reducida, cmap="YlGnBu", annot=False, cbar=True)
    plt.title("Mapa de Calor: Relación entre Temas y Palabras Clave")
    plt.xlabel("Palabras Clave")
    plt.ylabel("Categorías")
    plt.tight_layout()
    plt.show()

# Función principal
def main():
    archivo_csv = "articulos_20minutos.csv"
    try:
        df = preparar_datos(archivo_csv)

        # Visualizaciones
        distribucion_temas(df)
        evolucion_longitud_titulos(df)
        frecuencia_palabras_clave(df)
        mapa_calor_temas_palabras(df)
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar el script
if __name__ == "__main__":
    main()
