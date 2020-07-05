#!/bin/bash

set -euxo pipefail

# Initialize state by getting up to date
if [ ! -f "/data/scraper_state.json" ]
then
    echo "No state file, generating new one"
    python3 -m scraper.main --no-send=true
fi

crond -f
