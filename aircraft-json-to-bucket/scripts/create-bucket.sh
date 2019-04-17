#!/bin/bash 

source ./scripts/env.sh

gsutil mb gs://$OUTPUT_BUCKET

gsutil lifecycle set ./scripts/bucket-lifecycle.json gs://$OUTPUT_BUCKET

gsutil acl ch -u ${BUCKET_PUBLISHER_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com:W gs://$OUTPUT_BUCKET

