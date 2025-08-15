# avaktrahu/dataset
A curated, multi-modal dataset

## Overview

This repository provides a multi-modal dataset (images, text, etc.) packaged as a Docker image. The dataset is designed for reproducible research and easy integration into containerized workflows.

## Retrieving the Dataset

### Option 1: Pull and Extract Locally

Use the provided script to pull the dataset image and extract its contents:

```bash
./scripts/pull.sh latest-lts
```

This will download the latest long-term-support dataset image and copy its contents to the local `dataset/` directory.

### Option 2: Use as a Docker Volume

You can mount the dataset volume directly into your own container:

```bash
# Pull the image
docker pull avaktrahu/dataset:latest-lts

# Create a container with the dataset volume
docker run --name avaktrahu-dataset avaktrahu/dataset:latest-lts

# Mount the volume in your own container
docker run --volumes-from avaktrahu-dataset <your-image> <your-cmd>
```

## Building and Publishing

### Build and Push

To build and publish a new dataset image:

```bash
./scripts/push.sh [tag1 tag2 ...]
```

This will build the Docker image and push all specified tags to Docker Hub. The default tag `latest` is always updated.

### Dockerfile

The `Dockerfile` uses a minimal `scratch` base and copies the dataset into `/avaktrahu/dataset`. The directory is marked as a Docker volume for easy mounting.

## Release Cycle and Roadmap

### Release cadence

| Release Type | Cadence                | Includes                                                          |
| ------------ | ---------------------- | ----------------------------------------------------------------- |
| Thematic     | Annually or as needed  | Major changes, new modalities, large expansions, or restructuring |
| Incremental  | Quarterly or as needed | New data, minor schema changes, metadata updates                  |
| Patch        | As needed              | Bug fixes, corrupted file fixes, annotation corrections           |

### Available tags

| Release Tags | Availability | Release Notes                         |
| ------------ | ------------ | ------------------------------------- |
| `latest`     | Always       | Most recent (un)stable release        |
| `latest-lts` | Always       | Most recent long-term-support release |

## Contact & Contributions

For questions, issues, or contributions, please open an issue or pull request on GitHub.
