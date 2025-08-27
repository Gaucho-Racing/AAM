#!/bin/bash
service_name="aam"

# Get version from config.py
VERSION=$(grep -o 'VERSION: str = "[^"]*"' aam/config/config.py | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Error: Unable to extract version from aam/config/config.py"
    exit 1
fi

# Check if docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: docker is not installed.' >&2
  exit 1
fi

echo "Building container for $service_name v$VERSION"
# Build the docker container
docker build -t gauchoracing/$service_name:"$VERSION" -t gauchoracing/$service_name:latest --platform linux/amd64,linux/arm64 --push --progress=plain .