from pymongo import MongoClient
from model.person import Person
from model.newPerson import NewPerson
import json

class MongoDBOperations:
    def __init__(self, database_name, collection_name, port,username=None, password=None,host="localhost"):
        if username and password:
            self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/')
        else:
            self.client = MongoClient(f'mongodb://{host}:{port}/')
            
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def create_person(self, person: NewPerson):
        result = self.collection.insert_one(person.__dict__)
        return result

    def read_person(self, filter_criteria):
        result = self.collection.find(filter_criteria)
        data = list(result)
        return data

    def update_person(self, filter_criteria, update_data):
        result = self.collection.update_many(filter_criteria, {'$set': update_data})
        return result.modified_count

    def delete_person(self, filter_criteria):
        result = self.collection.delete_many(filter_criteria)
        return result.deleted_count
    
    def run_aggregation(self, pipeline):
        result = self.collection.aggregate(pipeline)
        return list(result)