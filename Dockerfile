# avaktrahu/dataset
# Dockerfile for building the dataset image

# A minimal base image to hold only the dataset
FROM scratch

# Docker takes care of mkdir
COPY ./dataset /avaktrahu/dataset

# Mark the dataset directory as a volume
VOLUME /avaktrahu/dataset

# Default command that does nothing but exits successfully.
CMD ["true"]
