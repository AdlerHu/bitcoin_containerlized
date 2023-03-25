# # crawler
# /home/adlerhu/.local/share/virtualenvs/bitcoin-7MbCzdvc/bin/python /home/adlerhu/bitcoin/crawl_latest_price.py &&

# # update historical data
# /home/adlerhu/.local/share/virtualenvs/bitcoin-7MbCzdvc/bin/python /home/adlerhu/bitcoin/update_latest_data.py &&

# # predict
# /home/adlerhu/.local/share/virtualenvs/bitcoin-7MbCzdvc/bin/python /home/adlerhu/bitcoin/predict.py &&

# # result
# /home/adlerhu/.local/share/virtualenvs/bitcoin-7MbCzdvc/bin/python /home/adlerhu/bitcoin/result.py &&

# # charts
# /home/adlerhu/.local/share/virtualenvs/bitcoin-7MbCzdvc/bin/python /home/adlerhu/bitcoin/charts.py


#!/bin/sh

docker run --name crawler --net=container:mysql crawler:1.0.0 && 
docker run --name etl --net=container:mysql etl:1.0.0 && 
docker run --name predict --net=container:mysql predict:1.0.0 && 
docker run --name result --net=container:mysql result:1.0.0 && 
docker run --name charts --net=container:mysql -v htmls:/charts/templates/ charts:1.0.0 && 
docker run --name webapp -d -p 5000:5000 -v htmls:/webapp/templates/ webapp:1.0.0 && 

docker container prune -f