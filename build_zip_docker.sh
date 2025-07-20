#!/bin/bash

set -e

PACKAGE_DIR="lambda_package"

rm -rf $PACKAGE_DIR
mkdir $PACKAGE_DIR

echo "Dockerを起動します"

docker run --rm \
  -v "$PWD":/var/task \
  python:3.12.4-slim \
  /bin/bash -c "
    cd /var/task && \
    pip install --upgrade pip && \
    pip install -r requirements.txt -t $PACKAGE_DIR
  "

cp -r application infrastructure lambda_function.py $PACKAGE_DIR/

echo "Zip化を行います"

cd $PACKAGE_DIR
zip -r ../lambda_package.zip .
cd ..

echo "✅ lambda_package.zip を作成しました。AWS Lambda にアップロードしてください。"
