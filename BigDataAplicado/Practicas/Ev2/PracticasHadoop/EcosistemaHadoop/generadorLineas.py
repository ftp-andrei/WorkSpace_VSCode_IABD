import random

def generate_random_file(filename, lines=5000, min_val=0, max_val=200):
    with open(filename, 'w') as file:
        for _ in range(lines):
            file.write(f"{random.randint(min_val, max_val)}\n")

# Llamada a la función para generar el archivo
generate_random_file("random_numbers.txt")