import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from collections import Counter
import time

# Cargar datos
archivo_csv = "articulos_20minutos.csv"
df = pd.read_csv(archivo_csv)

# Análisis descriptivo
def analisis_descriptivo(df):
    # Longitud de los títulos
    df['Longitud_Titulo'] = df['Título'].apply(len)
    
    print("Medidas estadísticas de la longitud de los títulos:")
    print(f"Media: {df['Longitud_Titulo'].mean():.2f}")
    print(f"Mediana: {df['Longitud_Titulo'].median():.2f}")
    print(f"Moda: {df['Longitud_Titulo'].mode().values[0]}")
    print(f"Desviación estándar: {df['Longitud_Titulo'].std():.2f}")
    
    # Histograma
    plt.hist(df['Longitud_Titulo'], bins=10, color='skyblue', edgecolor='black')
    plt.title("Distribución de la longitud de los títulos")
    plt.xlabel("Longitud")
    plt.ylabel("Frecuencia")
    plt.show()

# Análisis de frecuencia de palabras clave
def frecuencia_palabras(df):
    # Concatenar todos los títulos
    all_titles = " ".join(df['Título'])
    word_count = Counter(all_titles.split())
    common_words = word_count.most_common(10)
    
    print("Palabras más comunes en los títulos:")
    for word, count in common_words:
        print(f"{word}: {count}")
    
    # Visualizar en un gráfico de barras
    words, counts = zip(*common_words)
    plt.bar(words, counts, color='skyblue')
    plt.title("Palabras más comunes en los títulos")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Pruebas de hipótesis
def pruebas_hipotesis(df):
    # Crear categorías simuladas basadas en palabras clave
    # Esto sería más preciso si ya tuvieras las categorías en el archivo CSV
    df['Categoria'] = df['Título'].apply(lambda x: "Deportes" if "fútbol" in x.lower() else 
                                         ("Política" if "Ayuso" in x.lower() else "Otros"))
    
    # Agrupar por categoría
    grupos = df.groupby('Categoria')['Longitud_Titulo']
    
    # Imprimir estadísticas descriptivas por categoría
    for categoria, longitudes in grupos:
        print(f"\nCategoría: {categoria}")
        print(f"Media: {longitudes.mean():.2f}")
        print(f"Mediana: {longitudes.median():.2f}")
        print(f"Desviación estándar: {longitudes.std():.2f}")
    
    # Prueba de hipótesis: ANOVA (comparar más de dos categorías)
    categorias = [group for name, group in grupos]
    anova_result = stats.f_oneway(*categorias)
    print("\nResultado de la prueba ANOVA:")
    print(f"F-statistic: {anova_result.statistic:.2f}")
    print(f"p-value: {anova_result.pvalue:.4f}")
    
    if anova_result.pvalue < 0.05:
        print("Existen diferencias significativas entre las longitudes de los títulos de las categorías.")
    else:
        print("No se encontraron diferencias significativas entre las categorías.")

    # Mostrar un mensaje antes de cerrar
    print("\nEl programa se cerrará en 10 segundos...")
    time.sleep(10)

# Función principal
def main():
    # Cargar datos
    df = pd.read_csv(archivo_csv)

    # Análisis descriptivo
    analisis_descriptivo(df)
    
    # Frecuencia de palabras clave
    frecuencia_palabras(df)
    
    # Pruebas de hipótesis
    pruebas_hipotesis(df)

# Ejecutar el script
if __name__ == "__main__":
    main()