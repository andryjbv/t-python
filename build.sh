#!/bin/sh
# Common Setup, DO NOT MODIFY
cd /app
set -e

###############################################
# PROJECT DEPENDENCIES AND CONFIGURATION
###############################################
# Install project dependencies
pip install --no-cache-dir -r app/requirements.txt
pip install --no-cache-dir -r app/tests/requirements.txt
pip install --no-cache-dir ./app

# Configure environment variables (dummy values for tests)
export TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_API_KEY="apikey"
export TWILIO_API_SECRET="apisecret"
export TWILIO_FROM_NUMBER="+15005550006"
export TWILIO_TO_NUMBER="+15005550006"
export ASSISTANT_ID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

###############################################
# BUILD
###############################################
echo "================= 0909 BUILD START 0909 ================="
# No additional build steps required

echo "================= 0909 BUILD END 0909 ================="
