#!/bin/bash 

source ./scripts/env.sh

firebase functions:config:set receiver.version=v3.1.0
firebase functions:config:set receiver.refresh=5000
firebase functions:config:set receiver.history=120
firebase functions:config:set receiver.lat=0
firebase functions:config:set receiver.lon=0

firebase functions:config:set bucket.url=${PROJECT_ID}-aircraft-json
firebase functions:config:set bucket.device_id=k8s-receiver

firebase functions:config:get > functions/.runtimeconfig.json