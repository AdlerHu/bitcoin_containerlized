#!/bin/sh

# 完整程式列表 ('crawler' 'etl' 'predict' 'result' 'charts' 'webapp')

program=('crawler' 'etl' 'predict' 'result' 'charts' 'webapp')
version=('1.0.0' '1.0.0' '1.0.0' '1.0.0' '1.0.0' '1.0.0')

# tag docker images
for ((i=0;i<${#program[@]};i++))
do
    TAG_CMD="docker tag ${program[$i]}:${version[$i]} adlerhu/bitcoin_${program[$i]}:${version[$i]}"
    
    # 執行 docker build 命令
    $TAG_CMD
done

# push docker images to docker hub
for ((i=0;i<${#program[@]};i++))
do
    PUSH_CMD="docker push adlerhu/bitcoin_${program[$i]}:${version[$i]}"
    
    # 執行 docker build 命令
    $PUSH_CMD
done

# remove tagged images on local
for ((i=0;i<${#program[@]};i++))
do
    RM_CMD="docker rmi adlerhu/bitcoin_${program[$i]}:${version[$i]}"
    
    # 執行 docker build 命令
    $RM_CMD
done
