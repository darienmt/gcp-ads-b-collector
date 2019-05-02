#!/bin/bash 

export PROJECT_ID=$(gcloud config get-value project)

CURRENT_ACCOUNT=$(gcloud config list account --format "value(core.account)")

CURRENT_ACCOUNT=${CURRENT_ACCOUNT/@/_}

export CURRENT_ACCOUNT=${CURRENT_ACCOUNT//./_}
