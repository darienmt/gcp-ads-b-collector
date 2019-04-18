#!/bin/bash 

source ./scripts/env.sh

cp ${GOOGLE_APPLICATION_CREDENTIALS} ./key.json

docker build -t ${IMAGE_NAME} .

rm key.json