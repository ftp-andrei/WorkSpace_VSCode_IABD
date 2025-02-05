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


  