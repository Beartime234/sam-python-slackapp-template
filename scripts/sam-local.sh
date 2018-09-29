#!/usr/bin/env bash

PROFILE=beartimeworks # Your AWS profile that you have set up

export AWS_PROFILE=${PROFILE}

echo "Building application"
bash ./scripts/build.sh
clear
sam local start-api -t templates/template.yml --env-vars templates/variables.json