#!/bin/bash 

source ./scripts/env.sh

docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG}