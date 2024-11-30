import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.decomposition import LatentDirichletAllocation
import time

# Función para cargar y preparar los datos
def preparar_datos(archivo_csv):
    df = pd.read_csv(archivo_csv)
    
    # Verificar que exista la columna 'Título'
    if 'Título' not in df.columns:
        raise ValueError("El archivo CSV debe contener una columna llamada 'Título'.")
    
    # Eliminar filas con valores nulos en 'Título'
    df = df.dropna(subset=['Título'])
    return df

# Clasificación de documentos en categorías
def clasificar_documentos(df):
    # Suponiendo que tenemos una columna 'Categoría', si no existe, creamos una categoría de ejemplo
    if 'Categoría' not in df.columns:
        df['Categoría'] = df['Título'].apply(lambda x: "Deportes" if "fútbol" in x.lower() else 
                                             ("Política" if "Ayuso" in x.lower() else "Otros"))
    
    # Vectorización de los títulos de los artículos
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Título'])
    
    # Etiquetas de categorías (si no tienes etiquetas reales, puedes generar una de ejemplo como hice)
    y = df['Categoría']
    
    # División en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Entrenamiento del modelo (Regresión Logística)
    modelo = LogisticRegression()
    modelo.fit(X_train, y_train)
    
    # Predicciones
    y_pred = modelo.predict(X_test)
    
    # Mostrar resultados de clasificación
    print("Clasificación de documentos:")
    print(classification_report(y_test, y_pred))

# Análisis de temas con LDA (Latent Dirichlet Allocation)
def analisis_temas(df):
    # Usamos TF-IDF Vectorizer para obtener la matriz de términos
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    X_tfidf = tfidf_vectorizer.fit_transform(df['Título'])
    
    # Número de temas a identificar
    num_topics = 5
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(X_tfidf)
    
    # Visualización de los temas
    feature_names = np.array(tfidf_vectorizer.get_feature_names_out())
    
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic #{topic_idx + 1}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-11:-1]]))
    
    # Visualización de los temas en un gráfico de barras
    topic_words = []
    for topic_idx, topic in enumerate(lda.components_):
        topic_words.append([feature_names[i] for i in topic.argsort()[:-11:-1]])
    
    # Crear una estructura más fácil de visualizar
    topics_df = pd.DataFrame(topic_words, columns=[f"Palabra {i+1}" for i in range(10)])
    print("\nPalabras clave de los temas:")
    print(topics_df)

# Función de búsqueda de información por palabra clave
def buscar_articulos(df, palabra_clave):
    # Buscar artículos que contengan la palabra clave
    resultados = df[df['Título'].str.contains(palabra_clave, case=False, na=False)]
    
    if resultados.empty:
        print(f"No se encontraron artículos que contengan la palabra clave: '{palabra_clave}'.")
    else:
        print(f"Artículos que contienen '{palabra_clave}':")
        print(resultados[['Título']])

    # Mostrar un mensaje antes de cerrar
    print("\nLa búsqueda ha finalizado. El programa se cerrará en 5 segundos...")
    time.sleep(5)

# Función principal
def main():
    archivo_csv = "articulos_20minutos.csv"
    try:
        df = preparar_datos(archivo_csv)
        
        # Clasificación de documentos
        clasificar_documentos(df)
        
        # Análisis de temas
        analisis_temas(df)
        
        # Buscar artículos con palabra clave
        palabra_clave = input("Introduce una palabra clave para buscar artículos: ")
        buscar_articulos(df, palabra_clave)
    
    except Exception as e:
        print(f"Error: {e}")

# Ejecutar el script
if __name__ == "__main__":
    main()
