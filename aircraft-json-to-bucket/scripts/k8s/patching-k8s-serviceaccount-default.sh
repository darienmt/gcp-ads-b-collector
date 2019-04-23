#!/bin/bash 

source ./scripts/env.sh
source ./scripts/k8s/k8s_config


kubectl patch serviceaccount default \
-p '{"imagePullSecrets": [{"name": "gcr-json-key"}]}' \
--namespace ${K8S_NAMESPACE}
