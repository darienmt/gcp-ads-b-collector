#!/bin/bash 

source ./scripts/env.sh
source ./scripts/k8s/k8s_config
source ./scripts/receiver_url.sh

rm ./scripts/k8s/deployment.yaml
envsubst < ./scripts/k8s/deployment.template.yaml > ./scripts/k8s/deployment.yaml

kubectl apply -f ./scripts/k8s/deployment.yaml \
--namespace ${K8S_NAMESPACE}

