#!/bin/bash

set -e

PACKAGE_DIR="lambda_package"
LAMBDA_PYTHON_IMAGE="${LAMBDA_PYTHON_IMAGE:-python:3.13-slim}"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"

rm -rf $PACKAGE_DIR
mkdir $PACKAGE_DIR

echo "Dockerを起動します"
echo "Python image: $LAMBDA_PYTHON_IMAGE"
echo "Docker platform: $DOCKER_PLATFORM"

docker run --rm \
  --platform "$DOCKER_PLATFORM" \
  -v "$PWD":/var/task \
  "$LAMBDA_PYTHON_IMAGE" \
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
