#!/bin/bash

# Prüfen, ob das Docker-Netzwerk existiert
if ! docker network ls | grep -qw elastic; then
  echo "Netzwerk 'elastic' existiert nicht. Es wird erstellt..."
  docker network create elastic
else
  echo "Netzwerk 'elastic' ist bereits vorhanden."
fi

# Prüfen, ob das Docker-Volume existiert
if ! docker volume ls | grep -qw elasticsearch_data; then
  echo "Volume 'elasticsearch_data' existiert nicht. Es wird erstellt..."
  docker volume create elasticsearch_data
else
  echo "Volume 'elasticsearch_data' ist bereits vorhanden."
fi

docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.4

# Elasticsearch-Container starten
echo "Starte Elasticsearch-Container..."
docker run \
  --name es01 \
  --net elastic \
  -p 9200:9200 \
  -it \
  -m 32GB \
  --volume elasticsearch_data:/usr/share/elasticsearch/data \
  -e "ES_JAVA_OPTS=-Xms16g -Xmx16g" \ 
  docker.elastic.co/elasticsearch/elasticsearch:8.13.4

# 16GB RAM im Heap festlegen (Xms und Xmx) um OutOfMemoryError zu vermeiden

echo "Elasticsearch-Container wurde gestartet."


# if crt problem, use this command to start the container
# docker run --name es01 --net elastic -p 9200:9200 -it -m 32GB -e "ES_JAVA_OPTS=-Xms16g -Xmx16g" docker.elastic.co/elasticsearch/elasticsearch:8.13.4