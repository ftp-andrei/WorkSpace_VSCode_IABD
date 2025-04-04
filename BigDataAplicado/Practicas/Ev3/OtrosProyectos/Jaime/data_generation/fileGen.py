import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import boto3

fake = Faker()

def generate_sales_data(filename, num_rows=1500):
    with open(f'../data_bda/csv/{filename}', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Store ID", "Product ID", "Quantity Sold", "Revenue"])
        
        for _ in range(num_rows):
            date = random.choices([fake.date(), '', fake.color()], weights=[0.8, 0.15, 0.05])[0]

            store_id = random.choices([f'{random.randint(1, 1000)}', '', fake.color()], weights=[0.8, 0.15, 0.05])[0]

            product_id = random.choices([f'{random.randint(1, 100)}-{random.choice(['A','B','C'])}{random.randint(1, 200)}', '', fake.color()], weights=[0.8, 0.15, 0.05])[0]

            quantity_sold = random.choices([random.randint(1, 20), '', fake.color()], weights=[0.8, 0.15, 0.05])[0]

            revenue = random.choices([round(random.uniform(5.0, 100.0), 2), '', fake.color()], weights=[0.8, 0.15, 0.05])[0]
            
            writer.writerow([date, store_id, product_id, quantity_sold, revenue])

    print(f"Archivo '{filename}' generado con éxito.")

if __name__ == "__main__":
    generate_sales_data("ceseuve.csv")
    