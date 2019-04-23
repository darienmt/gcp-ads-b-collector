#!/bin/bash 

source ./scripts/env.sh
source ./scripts/k8s/k8s_config

kubectl create secret docker-registry gcr-json-key \
--docker-server=gcr.io \
--docker-username=_json_key \
--docker-password="$(cat ~/GCP_${PROJECT_ID}_$K8S_GCP_SERVICE_ACCOUNT.json)" \
--docker-email=any@valid.email \
--namespace ${K8S_NAMESPACE}