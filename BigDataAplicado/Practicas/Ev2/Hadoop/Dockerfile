# Dockerfile for Hadoop Cluster Setup
FROM python:3.10-slim-bullseye

USER root

# --------------------------------------------------------
# JAVA Installation
# --------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jdk curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# --------------------------------------------------------
# HADOOP Installation
# --------------------------------------------------------
ENV HADOOP_VERSION=3.4.1
ENV HADOOP_URL=https://downloads.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
ENV HADOOP_PREFIX=/opt/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV HADOOP_HOME=$HADOOP_PREFIX
ENV PATH="$HADOOP_PREFIX/bin:$PATH"

RUN set -eux && \
    curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz && \
    tar -xvf /tmp/hadoop.tar.gz -C /opt/ && \
    rm /tmp/hadoop.tar.gz && \
    ln -s /opt/hadoop-$HADOOP_VERSION/etc/hadoop /etc/hadoop && \
    mkdir -p /opt/hadoop-$HADOOP_VERSION/logs /hadoop-data

# --------------------------------------------------------
# Additional Tools (Sqoop, Flume, Pig)
# --------------------------------------------------------
RUN curl -fSL https://archive.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz -o sqoop.tar.gz && \
    ls -l sqoop.tar.gz && \
    tar -xf sqoop.tar.gz && \
    ls -l && \
    mv sqoop-1.4.7.bin__hadoop-2.6.0 /usr/local/sqoop

RUN curl -fSL https://dlcdn.apache.org/commons/lang/binaries/commons-lang3-3.17.0-bin.tar.gz -o commons-lang3.tar.gz && \
    tar -xf commons-lang3.tar.gz && \
    cp commons-lang3-3.17.0/commons-lang3-3.17.0.jar /usr/local/sqoop/lib && \
    rm -rf commons-lang3.tar.gz commons-lang3-3.17.0

# Install MySQL Connector
RUN curl -fSL http://ftp.ntu.edu.tw/MySQL/Downloads/Connector-J/mysql-connector-java-5.1.49.tar.gz -o mysql-connector.tar.gz && \
    tar -zxf mysql-connector.tar.gz && \
    mv mysql-connector-java-5.1.49/mysql-connector-java-5.1.49-bin.jar /usr/local/sqoop/lib && \
    rm -rf mysql-connector.tar.gz mysql-connector-java-5.1.49

# Install Flume
RUN curl -fSL https://dlcdn.apache.org/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz -o flume.tar.gz && \
    tar -xzf flume.tar.gz && \
    mv apache-flume-1.11.0-bin /usr/local/apache-flume && \
    rm -rf flume.tar.gz

# Install Pig
RUN curl -fSL https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz -o pig.tar.gz && \
    tar -xzf pig.tar.gz && \
    mv pig-0.17.0 /usr/local/pig && \
    rm -rf pig.tar.gz

ENV SQOOP_HOME=/usr/local/sqoop
ENV FLUME_HOME=/usr/local/apache-flume
ENV PIG_HOME=/usr/local/pig
ENV PATH="$SQOOP_HOME/bin:$FLUME_HOME/bin:$PIG_HOME/bin:$PATH"

# --------------------------------------------------------
# Copy Configuration Files
# --------------------------------------------------------
COPY conf/*.xml $HADOOP_CONF_DIR/

# --------------------------------------------------------
# Permissions
# --------------------------------------------------------
RUN chmod -R 755 /opt/hadoop-$HADOOP_VERSION /usr/local/sqoop /usr/local/apache-flume /usr/local/pig

USER root