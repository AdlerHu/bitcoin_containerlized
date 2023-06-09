#!/bin/sh

docker rm -f webapp
docker run --name crawler --net=container:mysql crawler:1.0.0 && 
docker run --name etl --net=container:mysql etl:1.0.0 && 
docker run --name predict --net=container:mysql predict:1.0.0 && 
docker run --name result --net=container:mysql result:1.0.0 && 
docker run --name charts --net=container:mysql -v htmls:/charts/templates/ charts:1.0.0
docker run --name webapp -d -p 5000:5000 -v htmls:/webapp/templates/ webapp:1.0.0

docker container prune -f
