#!/bin/bash 

source ./scripts/env.sh

gcloud iam service-accounts create $K8S_GCP_SERVICE_ACCOUNT

gcloud iam service-accounts keys create ~/GCP_${PROJECT_ID}_$K8S_GCP_SERVICE_ACCOUNT.json \
  --iam-account ${K8S_GCP_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
 --member serviceAccount:${K8S_GCP_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
 --role roles/storage.objectViewer