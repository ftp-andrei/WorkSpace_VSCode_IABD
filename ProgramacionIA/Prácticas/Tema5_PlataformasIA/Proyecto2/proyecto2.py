import random

def generar_prompts():
    # Solicitar datos al usuario
    print("Bienvenido a la aplicación de generación de prompts.")
    num_perros = int(input("¿Cuántas imágenes de perros deseas generar? "))
    num_gatos = int(input("¿Cuántas imágenes de gatos deseas generar? "))
    
    acciones = input("Introduce una lista de acciones separadas por comas (ejemplo: saltar, correr, dormir): ").split(",")
    acciones = [accion.strip() for accion in acciones if accion.strip()]  # Limpiar espacios
    
    estilo = input("¿Qué estilo deseas para las imágenes? (ejemplo: realista, caricatura, minimalista): ").strip()
    
    # Validar entradas
    if not acciones:
        print("Debe introducir al menos una acción. Intenta de nuevo.")
        return
    
    # Generar prompts
    prompts = []
    
    for _ in range(num_perros):
        accion_aleatoria = random.choice(acciones)
        prompts.append(f"A dog {accion_aleatoria} in a {estilo} style.")
    
    for _ in range(num_gatos):
        accion_aleatoria = random.choice(acciones)
        prompts.append(f"A cat {accion_aleatoria} in a {estilo} style.")
    
    # Mostrar resultados
    print("\nPrompts generados:")
    for prompt in prompts:
        print(prompt)
    
    return prompts

# Ejecutar la función
prompts_generados = generar_prompts()

# Mantener la consola abierta
input("\nPresiona Enter para salir...")
