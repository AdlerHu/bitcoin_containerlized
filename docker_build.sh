docker build -f /home/adlerhu/bitcoin_containerlized/crawler/crawler -t crawler:1.0.0 /home/adlerhu/bitcoin_containerlized/crawler/ &&
docker build -f /home/adlerhu/bitcoin_containerlized/etl/etl -t etl:1.0.0 /home/adlerhu/bitcoin_containerlized/etl/ &&
docker build -f /home/adlerhu/bitcoin_containerlized/predict/predict -t predict:1.0.0 /home/adlerhu/bitcoin_containerlized/predict/ &&
docker build -f /home/adlerhu/bitcoin_containerlized/result/result -t result:1.0.0 /home/adlerhu/bitcoin_containerlized/result/ &&
docker build -f /home/adlerhu/bitcoin_containerlized/charts/charts -t charts:1.0.0 /home/adlerhu/bitcoin_containerlized/charts/ &&
docker build -f /home/adlerhu/bitcoin_containerlized/webapp/webapp -t webapp:1.0.0 /home/adlerhu/bitcoin_containerlized/webapp/ 