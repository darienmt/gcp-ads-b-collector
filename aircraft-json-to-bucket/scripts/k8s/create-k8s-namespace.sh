#!/bin/bash 

source ./scripts/env.sh
source ./scripts/k8s/k8s_config

kubectl create namespace ${K8S_NAMESPACE}