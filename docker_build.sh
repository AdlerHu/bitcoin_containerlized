#!/bin/sh

program=('crawler' 'etl' 'predict' 'result' 'charts' 'webapp')
version=('1.0.0' '1.0.0' '1.0.0' '1.0.0' '1.0.0' '1.0.0')

for ((i=0;i<${#program[@]};i++))
do
    BUILD_CMD="docker build -f ${program[$i]}/${program[$i]} -t ${program[$i]}:${version[$i]} ${program[$i]}/"


    # 查看docke build 指令
    echo "${BUILD_CMD}"
    
    # 執行 docker build 命令
    $BUILD_CMD
done
