#!/bin/bash -x

# Builds the local image
docker build -t documentation-helper:0.1 .

# Start the container
docker run -d --name docs-h -p 8501:8501 docs-helper:0.1
