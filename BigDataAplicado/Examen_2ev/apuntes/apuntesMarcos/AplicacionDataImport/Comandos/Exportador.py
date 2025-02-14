import csv
import json

class DBExporter:
    def export_to_csv(self, result, filename='output.csv'):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            if isinstance(result, list) and result:
                if isinstance(result[0], dict):
                    headers = set()
                    for row in result:
                        headers.update(row.keys())
                    headers = list(headers)
                    writer.writerow(headers)
                    for row in result:
                        writer.writerow([row.get(col, '') for col in headers])
                elif isinstance(result[0], tuple):
                    writer.writerow(["Value"])
                    writer.writerows(result)
            elif isinstance(result, dict):
                writer.writerow(result.keys())
                writer.writerow(result.values())
    
    def export_to_json(self, result, filename='output.json'):
        with open(filename, 'w') as file:
            json.dump(result, file, indent=4, default=str)
    
    def export_neo4j_result(self, result, filename, filetype='json'):
        formatted_result = []
        for record in result:
            row = record.copy()
            if 'n' in row and isinstance(row['n'], dict):
                row.update(row.pop('n'))  # Extrae los valores del nodo en columnas separadas
            if 'roles' in row and isinstance(row['roles'], list):
                row['roles'] = ', '.join(row['roles'])  # Convierte la lista en una cadena separada por comas
            formatted_result.append(row)
        
        if filetype == 'csv':
            self.export_to_csv(formatted_result, filename)
        else:
            self.export_to_json(formatted_result, filename)
    
    def export_mongo_result(self, result, filename, filetype='json'):
        formatted_result = [{key: str(value) if key == '_id' else value for key, value in doc.items()} for doc in result]
        if filetype == 'csv':
            self.export_to_csv(formatted_result, filename)
        else:
            self.export_to_json(formatted_result, filename)
    
    def export_mysql_result(self, result, column_names, filename, filetype='json'):
        formatted_result = [dict(zip(column_names, row)) for row in result]
        if filetype == 'csv':
            self.export_to_csv(formatted_result, filename)
        else:
            self.export_to_json(formatted_result, filename)

    def export_dict(self, data, filename, filetype='json'):
        if not isinstance(data, dict):
            raise ValueError("El parámetro 'data' debe ser un diccionario.")

        if filetype == 'csv':
            self.export_to_csv(data, filename)
        else:
            self.export_to_json(data, filename)
