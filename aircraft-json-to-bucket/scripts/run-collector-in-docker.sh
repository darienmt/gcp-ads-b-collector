#!/bin/bash 

source ./scripts/env.sh
source ./scripts/receiver_url.sh

echo IMAGE: ${IMAGE_NAME} OUTPUT_BUCKER : ${OUTPUT_BUCKET}, RECEIVER_URL : ${RECEIVER_URL}
docker run -it \
  --env DEVICE_ID=docker-receiver \
  --env OUTPUT_BUCKET=${OUTPUT_BUCKET} \
  --env SAMPLING_PERIOD_SECONDS=${SAMPLING_PERIOD_SECONDS} \
  --env RECEIVER_URL=${RECEIVER_URL} \
  ${IMAGE_NAME}