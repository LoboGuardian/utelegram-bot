#!/bin/bash

# run.sh
#
# This script is used to execute the Python application using Pipenv.
# It ensures the application runs in the virtual environment managed
# by Pipenv, using the specified Python interpreter.
#
# Usage:
# 1. Ensure Pipenv is installed and dependencies are set up.
# 2. Make this script executable:
#    chmod +x run.sh
# 3. Run the script:
#    ./run.sh
#
# Note: Ensure Pipfile and Pipfile.lock exist in the project root.
# Dependencies should be installed using `pipenv install`.

# Variables for logging and error handling
LOG_FILE="app.log"


# Log function with levels (adapt as needed)
log() {
  local level="$1"  # e.g., info, debug, error
  local message="$2"
  echo "$(date +'%Y-%m-%d %H:%M:%S') - [$level] - [run.sh] - $message" | tee -a "$LOG_FILE"
}

# Check for Pipenv and install if necessary
if ! command -v pipenv &> /dev/null; then
  log info "Pipenv is not installed. Installing Pipenv..."
  python -m pip install pipenv
  if [ $? -ne 0 ]; then
    log error "Failed to install Pipenv. Please install it manually."
    exit 1
  fi
fi

# Check for Pipfile  or requirements.txt
if [ ! -f "Pipfile" ]; then
  if [ -f "requirements.txt" ]; then
    log info "Pipfile not found. Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
      log error "Failed to install dependencies from requirements.txt. Check requirements.txt."
      exit 1
    else
      log info "Dependencies installed successfully from requirements.txt."
    fi
  else
    log error "Pipfile and requirements.txt not found. Please ensure you're in the project root directory."
    exit 1
  fi
fi

# Check Python interpreter (optional)
py_version=$(python3 --version 2>&1)
log info "Python version: $py_version"

# Temporary file to store the previous hash
HASH_FILE="app_previous_hash.log"

# Check if the hash file exists
if [ -f "$HASH_FILE" ]; then
  PREVIOUS_HASH=$(cat "$HASH_FILE")
fi

# Calculate the current hash
current_hash=$(sha256sum Pipfile.lock | awk '{print $1}')

# Compare the hashes and install dependencies if necessary
if [ "$current_hash" != "$PREVIOUS_HASH" ]; then
  log info "Pipfile.lock has changed. Installing dependencies..."

  pipenv install
  if [ $? -ne 0 ]; then
    log error "Failed to install dependencies. Check Pipfile and Pipfile.lock."
    exit 1
  else
    log info "Dependencies installed successfully."
    # Update requirements.txt if necessary (e.g., based on your project setup)
    pipenv requirements > requirements.txt
    log info "Update requirements file."
  fi
  # Update the previous hash
  echo "$current_hash" > "$HASH_FILE"
else
  log info "Pipfile.lock has not changed. Skipping dependency installation."
fi

# Source environment variables (optional)
# source .env  # Uncomment this if needed

# Activate Pipenv environment
log info "Starting the Python application..."
pipenv run python src/main.py

# Capture and handle specific exit code (optional)
exit_code=$?
if [ $exit_code -ne 0 ]; then
  log error "Application failed to start (exit code: $exit_code). Check the log for details."
else
  log info "Application finished successfully."
fi