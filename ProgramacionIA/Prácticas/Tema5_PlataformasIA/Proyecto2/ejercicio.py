import random
from datetime import datetime
import os
from diffusers import StableDiffusionXLPipeline
import torch
import pandas as pd

pipe = StableDiffusionXLPipeline.from_pretrained("segmind/SSD-1B", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe = pipe.to("cuda")  # Asegúrate de usar la GPU si está disponible

# Función para generar prompts
def generar_prompts():
  num_perros = int(input("¿Cuántas imágenes de perros deseas generar? "))
  num_gatos = int(input("¿Cuántas imágenes de gatos deseas generar? "))

  acciones = input("Introduce una lista de acciones separadas por comas (ejemplo: jump, run, sleep): ").split(",")
  acciones = [accion.strip() for accion in acciones if accion.strip()]  # Limpiar espacios

  estilo = input("¿Qué estilo deseas para las imágenes? (ejemplo: realistic, cartoonish, minimalist): ").strip()

  # Validar entradas
  if not acciones:
    print("Debe introducir al menos una acción. Intenta de nuevo.")
    return []

    # Generar prompts
  prompts = []
  for i in range(num_perros):
    accion_aleatoria = random.choice(acciones)
    prompts.append(f"A {random.choice(['small', 'large', 'fluffy'])} dog {accion_aleatoria} in a {estilo} style, in a {random.choice(['park', 'beach', 'snowfield'])}.")

  for i in range(num_gatos):
    accion_aleatoria = random.choice(acciones)
    prompts.append(f"A {random.choice(['small', 'large', 'fluffy'])} cat {accion_aleatoria} in a {estilo} style, in a {random.choice(['park', 'beach', 'snowfield'])}.")

  return prompts

def creacionCarpetas():
  images = "images"
  perro = "perros"
  gato = "gatos"

  if not os.path.exists(images):
    os.makedirs(images)
    print(f"Carpeta '{images}' creada.")

  perro_path = os.path.join(images, perro)
  if not os.path.exists(perro_path):
    os.makedirs(perro_path)
    print(f"Carpeta '{perro_path}' creada.")

  gato_path = os.path.join(images, gato)
  if not os.path.exists(gato_path):
    os.makedirs(gato_path)
    print(f"Carpeta '{gato_path}' creada.")

def esPerro(imagen):
  picture_question = pipeline(task="visual-question-answering", model="dandelin/vilt-b32-finetuned-vqa")
  resultado = picture_question(image=imagen, question="is it a dog?")
  print(resultado)
  return resultado[0]['answer']


# Función para guardar imágenes simuladas
def generar_imagenes(prompts):
  creacionCarpetas()

  images = "images"
  perro = "perros"
  gato = "gatos"
  df= pd.DataFrame()
  for i, prompt in enumerate(prompts):
    print(f"Generando imagen para el prompt: {prompt}")
    # Prompt negativos
    neg_prompt = "ugly, blurry, poor quality, distorted, low resolution, grainy, pixelated, out of focus, poorly lit, awkward anatomy, bad proportions, unbalanced, noisy, blurry background, bad color scheme, poorly composed, overexposed, underexposed, unnatural lighting, unrealistic, unnatural shadows, incomplete, malformed, distorted features"

    # Generamos la imagen
    image = pipe(prompt=prompt, negative_prompt=neg_prompt).images[0]
    if esPerro(image) == "yes":
      nombre_archivo = f"{images}/{perro}/imagen_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
      tipo_animal = "Perro"
    else:
      nombre_archivo = f"{images}/{gato}/imagen_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
      tipo_animal = "Gato"

    df = pd.concat([df, pd.DataFrame({"NombreFichero": [nombre_archivo], "TipoAnimal": [tipo_animal]})], ignore_index=True)

    print(f"Imagen guardada como '{nombre_archivo}'")
    image.save(nombre_archivo)  # Guardar imagen
  df.to_csv("Animales.csv", index=False)


def main():
    prompts = generar_prompts()

    if prompts:
        generar_imagenes(prompts)
    else:
        print("No se han generado prompts. Finalizando programa.")

if __name__ == "__main__":
    main()