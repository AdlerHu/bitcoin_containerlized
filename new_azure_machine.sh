#!/bin/sh

apt-get update

# install Docker
apt-get install  -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

apt-get remove -y vim vim-runtime vim-tiny vim-common vim-scripts vim-doc
apt-get install -y vim

mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# create docker volume
docker volume create mysql
docker volume create htmls

# pull needed images
docker pull adlerhu/bitcoin_crawler:1.0.0
docker pull adlerhu/bitcoin_etl:1.0.0
docker pull adlerhu/bitcoin_predict:1.0.0
docker pull adlerhu/bitcoin_result:1.0.0
docker pull adlerhu/bitcoin_charts:1.0.0
docker pull adlerhu/bitcoin_webapp:1.0.0

mkdir /home/azureuser/bitcoin_containerlized/
touch /home/azureuser/bitcoin_containerlized/mysql.yml
touch /home/azureuser/bitcoin_containerlized/daily.sh

echo "version: '3.3'
services:

  mysql:
      image: mysql:8.0
      container_name: mysql
      command: mysqld --default-authentication-plugin=mysql_native_password
      ports: 
          - 3306:3306
   
      environment:
          MYSQL_DATABASE: mydb
          MYSQL_USER: user
          MYSQL_PASSWORD: test
          MYSQL_ROOT_PASSWORD: test

      volumes:
          - mysql:/var/lib/mysql
      networks:
          - dev

  phpmyadmin:
      image: phpmyadmin/phpmyadmin:5.1.0
      container_name: phpmyadmin
      links: 
          - mysql:db
      ports:
          - 8000:80
      depends_on:
        - mysql
      networks:
          - dev

networks:
  dev:

volumes:
  mysql:
    external: true" >> /home/azureuser/bitcoin_containerlized/mysql.yml
	
echo "#!/bin/sh

docker run --name crawler --net=container:mysql adlerhu/bitcoin_crawler:1.0.0 && 
docker run --name etl --net=container:mysql adlerhu/bitcoin_etl:1.0.0 && 
docker run --name predict --net=container:mysql adlerhu/bitcoin_predict:1.0.0 && 
docker run --name result --net=container:mysql adlerhu/bitcoin_result:1.0.0 && 
docker run --name charts --net=container:mysql -v htmls:/charts/templates/ adlerhu/bitcoin_charts:1.0.0

docker container prune -f" >> /home/azureuser/bitcoin_containerlized/daily.sh

chown -R azureuser:azureuser /home/azureuser/bitcoin_containerlized/
usermod -aG docker azureuser
