docker build -t hadoop-bda:3.4.1 .
docker-compose up -d



  ### CREACION DE NUEVO NODO
  # ponemos comando:
  # docker-compose down/up

  #  datanode2:
  #    build: ./Datanode
  #    container_name: datanode2
  #    hostname: datanode2
  #    depends_on:
  #       - namenode
  #     ports: # se cambia el puerto de la izq
  #       - "9865:9864" # DataNode Web UI
  #     volumes:
  #       - hadoop_datanode2:/hadoop/dfs/data
  #     networks:
  #       hadoop_network:
  #         aliases:
  #           - datanode2




------------------------------
        APUNTES hadoop
------------------------------

docker exec -it namenode bin/bash -> Nos metemos dentro del namenode
cd home -> Nos moveremos a la carpeta home (si no esta la creamos [mkdir home])
docker cp D:\WorkSpace_VSCode_IABD\BigDataAplicado\Practicas\Ev2\PracticasHadoop\EcosistemaHadoop\random_numbers.txt namenode:/home -> Para subir al namenode

hdfs dfs -mkdir /home -> Crea el directorio home
hdfs dfs -put /home/archivo.txt /home/ -> Subimos el archivo a HDFS
hdfs dfs -ls [opcional ruta] -> Vemos el contenido con permisos
hdfs dfs -get /home/archivo.txt C:/ -> Descargamos desde HDFS al namenode (tambien se puede con -copyToLocal)
docker cp namenode:/archivo.txt C:/Users/Andrei/Desktop/archivo.txt -> Desde el namenode a local




# SI DA CONEXION ERROR AL SUBIR A HDFS:

hdfs namenode -format  # SOLO si es la primera vez, ¡esto borra datos en HDFS!
hdfs --daemon start namenode
hdfs --daemon start datanode





http://localhost:9870/explorer.html#/ -> HDFS Browser


COMANDOS UTILES HDFS
----------------------
hdfs dfs -get /user/tu_usuario/archivo.txt /home/ -> Descargar el archivo de HDFS al contenedor

hdfs dfs -put /home/archivo.txt /home/ -> Subimos el archivo a HDFS

hdfs dfs -cat /user/tu_usuario/archivo.txt -> Ver el contenido del archivo en HDFS

hdfs dfs -cp /user/tu_usuario/archivo.txt /user/backup/ -> Copiar un archivo dentro de HDFS

hdfs dfs -mv /user/tu_usuario/archivo.txt /user/backup/ -> Mover un archivo dentro de HDFS

hdfs dfs -rm /user/tu_usuario/archivo.txt -> Eliminar un archivo en HDFS
