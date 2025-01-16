import os
import random
from faker import Faker

fake = Faker()

with open("andrei.txt", "w") as f:
    for _ in range(1000):
        f.write(" ".join(fake.words(random.randint(2, 5))) + "\n")