import pandas as pd

def dividir_grupos():
    try:
        # 1. Leer el archivo Excel (¡asegúrate de que el nombre es correcto!)
        datos = pd.read_excel('dataset.xlsm', sheet_name='Original')  # o el nombre de tu hoja

        # 2. Verificar columnas (por si los nombres son diferentes)
        columna_edad = 'Age'
        columna_genero = 'Gender'
        
        if columna_edad not in datos.columns or columna_genero not in datos.columns:
            print("⚠️ Error: Las columnas deben llamarse 'age' y 'gender'")
            print("Columnas encontradas:", datos.columns.tolist())
            return None
        
        # 3. Limpiar datos (por si hay mayúsculas/minúsculas inconsistentes)
        datos[columna_genero] = datos[columna_genero].str.strip().str.capitalize()
        
        # 4. Filtrar grupos
        grupos = {
            'Joven': {
                'Male': datos[(datos[columna_edad] <= 40) & (datos[columna_genero] == 'M')],
                'Female': datos[(datos[columna_edad] <= 40) & (datos[columna_genero] == 'F')]
            },
            'Mayor': {
                'Male': datos[(datos[columna_edad] > 40) & (datos[columna_genero] == 'M')],
                'Female': datos[(datos[columna_edad] > 40) & (datos[columna_genero] == 'F')]
            }
        }
        
        # 5. Mostrar resultados
        print("\n=== RESUMEN DE GRUPOS ===")
        for grupo_edad, generos in grupos.items():
            print(f"\n🔹 Grupo {grupo_edad}:")
            for genero, df in generos.items():
                print(f"   {genero}: {len(df)} registros")
        
        return grupos
    
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'dataset.xlsm'.")
        print("   → Verifica que el archivo esté en la misma carpeta que tu script.")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return None

# Ejecutar y guardar resultados
resultado = dividir_grupos()