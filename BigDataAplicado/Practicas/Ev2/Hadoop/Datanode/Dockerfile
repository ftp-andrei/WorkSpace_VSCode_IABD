FROM hadoop-bda:3.4.1

HEALTHCHECK CMD curl -f http://localhost:9864/ || exit 1

ENV HDFS_CONF_dfs_datanode_data_dir=file:///hadoop/dfs/data
USER root
RUN mkdir -p /hadoop/dfs/data
VOLUME /hadoop/dfs/data

ADD run.sh /run.sh
RUN sed -i 's/\r$//g' /run.sh
RUN chmod a+x /run.sh

EXPOSE 9864

CMD ["./run.sh"]