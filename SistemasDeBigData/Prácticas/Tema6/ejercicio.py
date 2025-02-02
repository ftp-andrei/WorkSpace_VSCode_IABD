import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv("SampleSuperstore.csv")

# Mostrar información general del dataset
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
df.info()

# Descripción estadística
print(df.describe())

# Contar valores nulos
print("Valores nulos por columna:")
print(df.isnull().sum())

# Histogramas de Ventas y Ganancias
sns.set(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.histplot(df["Sales"], bins=30, kde=True, ax=axes[0])
axes[0].set_title("Distribución de Ventas")
axes[0].set_xlabel("Ventas")
sns.histplot(df["Profit"], bins=30, kde=True, ax=axes[1])
axes[1].set_title("Distribución de Ganancias")
axes[1].set_xlabel("Ganancias")
plt.tight_layout()
plt.show()

# Productos más vendidos
plt.figure(figsize=(12, 5))
top_products = df["Sub-Category"].value_counts().head(10)
sns.barplot(x=top_products.index, y=top_products.values, palette="viridis")
plt.xticks(rotation=45)
plt.title("Top 10 Productos Más Vendidos")
plt.xlabel("Sub-Categoría")
plt.ylabel("Cantidad de Ventas")
plt.show()

# Relación entre Ventas y Ganancia
plt.figure(figsize=(10, 5))
sns.scatterplot(x=df["Sales"], y=df["Profit"], alpha=0.5)
plt.title("Relación entre Ventas y Ganancia")
plt.xlabel("Ventas")
plt.ylabel("Ganancia")
plt.show()

# Tabla cruzada entre Región y Producto
region_product_table = pd.crosstab(df["Region"], df["Sub-Category"])
plt.figure(figsize=(12, 6))
sns.heatmap(region_product_table, cmap="coolwarm", linewidths=0.5)
plt.title("Mapa de Calor: Ventas por Región y Sub-Categoría")
plt.xlabel("Sub-Categoría")
plt.ylabel("Región")
plt.xticks(rotation=45)
plt.show()

# Matriz de correlación
correlation_matrix = df[["Sales", "Quantity", "Discount", "Profit"]].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlaciones entre Variables Numéricas")
plt.show()

# Análisis de valores atípicos con boxplots
num_vars = ["Sales", "Profit", "Quantity", "Discount"]
plt.figure(figsize=(12, 8))
for i, var in enumerate(num_vars, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(y=df[var])
    plt.title(f"Boxplot de {var}")
plt.tight_layout()
plt.show()

# Identificación de valores atípicos con IQR
outliers = {}
for var in num_vars:
    Q1 = df[var].quantile(0.25)
    Q3 = df[var].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers[var] = df[(df[var] < lower_bound) | (df[var] > upper_bound)][var]

print("Valores atípicos identificados:")
for var, outlier_values in outliers.items():
    print(f"{var}: {len(outlier_values)} valores atípicos")

# Resumen de Indicadores
ventas_por_region = df.groupby("Region")["Sales"].sum()
print("Ventas totales por región:")
print(ventas_por_region)

producto_mas_vendido = df["Sub-Category"].value_counts().idxmax()
print(f"Producto más vendido: {producto_mas_vendido}")

promedio_ganancia_por_region = df.groupby("Region")["Profit"].mean()
print("Promedio de ganancia por región:")
print(promedio_ganancia_por_region)