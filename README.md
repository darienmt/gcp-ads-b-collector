# gcp-ads-b-collector
Collecting ADS-B data from dump1090. 

# Overview

There are a few experiments I've been doing regarding how to collect ADS-B data and share it or process the data as a hobbie. Here are some description of each directory:

- **[aircraft-json-collector](./aircraft-json-collector)**: Python script to publish `data/aircraft.json` to  [GCP PubSub Topic](https://cloud.google.com/pubsub/).

- **[topic-cloud-function](./topic-cloud-function)**: [GCP Cloud function](https://cloud.google.com/functions/) to process that topic and insert it on [Big Query](https://cloud.google.com/bigquery/)

- **[aircraft-json-to-bucket](./aircraft-json-to-bucket)**: Python script to publish `data/aircraft.json` to a [GCP Storage](https://cloud.google.com/storage/).

- **[aircraft-firebase](./aircraft-firebase)**: [Firebase](https://firebase.google.com/) hosting and functions modifications to [dump1090 public_html](https://github.com/flightaware/dump1090/tree/master/public_html) to be able to run this application on Firebase and consume the `data/aircraft.json` information stored on a GCP Storabe bucket.
