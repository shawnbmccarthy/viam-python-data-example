#!/usr/bin/env bash

if [[ ! -d ./.venv || ! -d ./venv ]]; then
  python3 -m venv .venv &> /dev/null
  .venv/bin/pip install -r ./requirements.txt &> /dev/null
fi

if [[ -f ./env.dev.sh ]]; then
  echo "using dev environment"
  source ./env.dev.sh
else
  source ./env.sh
fi

./.venv/bin/python3 main.py -o "${ORG_ID}" -a "${ORG_API_KEY}" -i "${ORG_API_ID}"  -c "ais" -s "2024-01-23T08:00:00" -e "2024-01-23T09:00:00"