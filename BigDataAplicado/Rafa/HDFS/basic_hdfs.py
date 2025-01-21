import csv
import os
from pywebhdfs.webhdfs import PyWebHdfsClient
# pip install pywebhdfs
from pprint import pprint
#10.2.14.251
#192.168.50.251
hdfs = PyWebHdfsClient(host='localhost',port='9870', user_name='root')
content=""
with open("Tema 3/Hadoop/data/train.csv", 'r') as file:
            content = file.read()

#HDFS
#/data/claims.csv
my_file = '/bda_test/claims.csv'
hdfs.create_file(my_file, content)

#Posterior, tras ejecutar el job.
data=hdfs.read_file("user/root/nulos/part-m-00000")
with open("result.csv", 'w') as file:
    file.write(data)

#c:\Windows\System32\Drivers\etc\hosts
#127.0.0.1 namenode
#127.0.0.1 datanode
#127.0.0.1 resourcemanager
#127.0.0.1 nodemanager