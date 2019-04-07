#!/bin/bash 

source ./scripts/env.sh

gcloud iam service-accounts create $TEST_RUNNER_ACCOUNT

gcloud projects add-iam-policy-binding $PROJECT_ID --member "serviceAccount:${TEST_RUNNER_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"

gcloud iam service-accounts keys create ~/GCP_${PROJECT_ID}_$TEST_RUNNER_ACCOUNT.json --iam-account ${TEST_RUNNER_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com