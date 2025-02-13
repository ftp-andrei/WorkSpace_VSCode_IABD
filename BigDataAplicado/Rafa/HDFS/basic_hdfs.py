import csv
import os
from pywebhdfs.webhdfs import PyWebHdfsClient
from pprint import pprint
hdfs = PyWebHdfsClient(host='localhost',port='9870', user_name='root')
content=""
with open("Tema 3/Hadoop/data/train.csv", 'r') as file:
            content = file.read()

#HDFS
my_file = '/data/claims.csv'
hdfs.create_file(my_file, content)
#Posterior, tras ejecutar el job.


dirData= hdfs.list_dir('/data/output_directory')

data=''
for file in dirData['FileStatuses']['FileStatus']:
    data+=hdfs.read_file("/data/output_directory/"+file['pathSuffix']).decode('utf-8')

with open("result.csv", 'w',encoding="utf-8") as file:
    file.write(data)

