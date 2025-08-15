#!/bin/bash

# avaktrahu/dataset
# Shell script to pull and extract dataset from Docker image

# =============================================================================
# Configuration
#

IMAGE_REPOSITORY="avaktrahu/dataset"
IMAGE_TAG="${1:-latest}"            # Accept image tag as an argument

SOURCE_VOLUME="/avaktrahu/dataset"  # Absolute path inside the container
TARGET_VOLUME="dataset"             # Path relative to workspace

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

# Ensure local directory exists
mkdir -p "$TARGET_VOLUME"

# =============================================================================
# Main
#

# Pull the Docker image
docker pull "$IMAGE_REPOSITORY:$IMAGE_TAG"

# Mount a temporary container
CONTAINER_ID=$(docker create "$IMAGE_REPOSITORY:$IMAGE_TAG")

# Copy dataset from container to local directory
docker cp "${CONTAINER_ID}:$SOURCE_VOLUME/." "$TARGET_VOLUME"

# Clean up
docker rm "$CONTAINER_ID"
docker rmi "$IMAGE_REPOSITORY:$IMAGE_TAG"
