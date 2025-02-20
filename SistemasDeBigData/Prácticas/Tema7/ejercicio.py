import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report, confusion_matrix

# Cargar datos
file_path = "PREC_2021_Provincias.csv"
df = pd.read_csv(file_path, sep=";")


# Preprocesamiento de datos
# Seleccionamos las columnas relevantes para predecir precipitaciones anuales altas/bajas
df["HighPrecipitation"] = (df["anual"] > 1000).astype(int)  # Etiquetamos si la precipitación anual es >1000 mm
X = df.iloc[:, 2:14]  # Datos de enero a diciembre
y = df["HighPrecipitation"]  # Etiqueta de clasificación

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar un modelo (Random Forest en este caso)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Realizar predicciones
y_pred = clf.predict(X_test)

# Evaluar el modelo usando las métricas
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Mostrar resultados
print("Precisión:", precision)
print("Recall:", recall)
print("F1-Score:", f1)
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred))
print("\nMatriz de Confusión:")
print(confusion_matrix(y_test, y_pred))