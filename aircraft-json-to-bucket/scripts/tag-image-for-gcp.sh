#!/bin/bash 

source ./scripts/env.sh

docker tag ${IMAGE_NAME} \
  gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}