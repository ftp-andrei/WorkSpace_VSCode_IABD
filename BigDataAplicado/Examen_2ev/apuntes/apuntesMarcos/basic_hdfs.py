from pywebhdfs.webhdfs import PyWebHdfsClient


hdfs = PyWebHdfsClient(host='127.0.0.1',port='9870', user_name='root')
content=""
with open("NumerosAleatorios.txt", 'r') as file:
            content = file.read()

#HDFS
my_file = 'NumerosAleatorios.txt'
hdfs.create_file(my_file, content)