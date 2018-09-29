#!/usr/bin/env bash

SECRETS_NAME="<REPLACE_ME>"  # The name of the secret in secrets manager that stores
AWS_PROFILE="<REPLACE_ME>"  # Your AWS profile that you have set up

# Fix for pytest wont be able to import applications
export PYTHONPATH=src/

# Env variables
export SECRETS_NAME=${SECRETS_NAME}  # The name of secrets
export STAGE="local-dev"
export AWS_PROFILE=${AWS_PROFILE}

echo "Running Tests"
pipenv run python -m pytest tests/ -v