#!/bin/bash

set -euxo pipefail

# Initialize state by getting up to date
python3 -m scraper.main --no-send=true

crond -f
