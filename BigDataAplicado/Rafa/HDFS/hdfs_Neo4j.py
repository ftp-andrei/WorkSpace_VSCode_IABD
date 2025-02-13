#pip install pymongo
#pip install Faker
from pywebhdfs.webhdfs import PyWebHdfsClient
from utils.JsonHelper import *
from data.neo4j_operations import *
import json
from faker import Faker
import random

uri = "bolt://localhost:7687"  
user = "neo4j"
password = "my-secret-pw"

neo4j_crud = Neo4jCRUD(uri, user, password)

fake = Faker()

node_properties = {"name": fake.name(), "type": fake.mime_type(), "cantidad":random.randint(18, 65)}
created_node = neo4j_crud.create_node("ExampleNode", node_properties)


nodes = neo4j_crud.read_nodes("ExampleNode")
dataNeo4j=[]
for element in nodes:
    dataNeo4j.append(element._properties)
content= json.dumps(dataNeo4j,indent=4)

hdfs = PyWebHdfsClient(host='localhost',port='9870', user_name='root')

#HDFS
my_file = '/data/dataNode.json'
hdfs.create_file(my_file,content)


dirData= hdfs.list_dir('/data')

data=''
for file in dirData['FileStatuses']['FileStatus']:
    data+=hdfs.read_file("/data/output_directory/"+file['pathSuffix']).decode('utf-8')

with open("result.csv", 'w',encoding="utf-8") as file:
    file.write(data)
