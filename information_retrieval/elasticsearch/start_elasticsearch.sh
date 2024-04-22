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

# Elasticsearch-Container starten
echo "Starte Elasticsearch-Container..."
docker run -d \
  --name es01 \
  --net elastic \
  -p 9200:9200 \
  --memory 16g \
  --volume elasticsearch_data:/usr/share/elasticsearch/data \
  -e "discovery.type=single-node" \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.2

echo "Elasticsearch-Container wurde gestartet."