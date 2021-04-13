#!/bin/bash

set -euxo pipefail

curl https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest > gmail_v1.json

docker build -t scraper .

docker save scraper > scraper.tar
