#!/bin/bash

# avaktrahu/dataset
# Shell script to build and push dataset Docker image

# =============================================================================
# Configuration
#

IMAGE_REPOSITORY="avaktrahu/dataset"

# Accept tags as command line arguments
TAGS=("latest" "$@")

# =============================================================================
# Setup
#

# Exit immediately if a command exits with a non-zero status
set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# =============================================================================
# Main
#

# Build the Docker image with all tags
BUILD_ARGS=""
for TAG in "${TAGS[@]}"; do
    BUILD_ARGS+=" -t $IMAGE_REPOSITORY:$TAG"
done
docker build $BUILD_ARGS .

# Prompt for Docker Hub login if not already logged in
if ! docker info 2>/dev/null | grep -q 'Username:'; then
    echo "Docker Hub login required."
    docker login
fi

# Push all tags to Docker Hub
for TAG in "${TAGS[@]}"; do
    docker push "$IMAGE_REPOSITORY:$TAG"
done
