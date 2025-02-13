#pip install pymongo
#pip install Faker
from model.person import Person 
from model.newPerson import NewPerson
from data.mongo_operations import MongoDBOperations
from faker import Faker
from pywebhdfs.webhdfs import PyWebHdfsClient
from utils.JsonHelper import *
from bson import json_util

def parse_json(data):
    return json_util.dumps(data,indent=4)

fake = Faker()

mongo_operations = MongoDBOperations('federacion', 'arbitros','7777',username="mongoadmin",password="secret")

personJohn = NewPerson(name=fake.name(), age=fake.date_of_birth().__str__(), email=fake.email(),info=fake.word())
personJane = NewPerson(name=fake.name(), age=fake.date_of_birth().__str__(), email=fake.email(),info=fake.word())


mongo_operations.create_person(personJohn)
mongo_operations.create_person(personJane)

all_persons = mongo_operations.read_person({})
print("All persons:", all_persons)
content=parse_json(all_persons)

hdfs = PyWebHdfsClient(host='localhost',port='9870', user_name='root')

#HDFS
my_file = '/data/dataPerson.json'
hdfs.create_file(my_file,content )


dirData= hdfs.list_dir('/data')

data=''
for file in dirData['FileStatuses']['FileStatus']:
    data+=hdfs.read_file("/data/output_directory/"+file['pathSuffix']).decode('utf-8')

with open("result.csv", 'w',encoding="utf-8") as file:
    file.write(data)
