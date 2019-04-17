#!/bin/bash 

source ./scripts/env.sh

gcloud iam service-accounts create $BUCKET_PUBLISHER_ACCOUNT

gcloud iam service-accounts keys create ~/GCP_${PROJECT_ID}_$BUCKET_PUBLISHER_ACCOUNT.json \
  --iam-account ${BUCKET_PUBLISHER_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com