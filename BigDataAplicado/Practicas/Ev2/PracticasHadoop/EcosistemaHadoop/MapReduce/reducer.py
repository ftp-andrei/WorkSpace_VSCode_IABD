#!/usr/bin/env python
import sys

# Leemos todos los números
numbers = []

for line in sys.stdin:
    numbers.append(int(line.strip()))

# Ordenamos los números
numbers.sort()

# Calculamos la mediana
n = len(numbers)
if n % 2 == 1:
    # Si hay un número impar de elementos, la mediana es el del medio
    median = numbers[n // 2]
else:
    # Si hay un número par de elementos, la mediana es el promedio de los dos del medio
    median = (numbers[n // 2 - 1] + numbers[n // 2]) / 2.0

# Imprimimos la mediana
print(f"Median: {median}")
