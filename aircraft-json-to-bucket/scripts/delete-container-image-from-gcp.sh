#!/bin/bash 

source ./scripts/env.sh

gcloud container images delete \
  gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${IMAGE_TAG} \
  --force-delete-tags