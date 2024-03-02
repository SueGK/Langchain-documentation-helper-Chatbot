# LangChain Documentation Helper

<img src="https://github.com/SueGK/documentation-helper/blob/local-docker/Bot.gif" width="650" height="650"/>

## Overview

The LangChain Documentation Helper, built with Langchain, pinecone and streamlit, is a web-based application designed to facilitate learning and exploration of LangChain by leveraging generative AI. By integrating with Pinecone, a vector database, this application provides an efficient and intuitive way to query and interact with LangChain's official documentation.

## Environment Setup

To securely manage application configurations and sensitive credentials, this project uses environment variables stored in a .env file at the root of the project directory. Before running the application, you must create this file and populate it with the necessary keys.

**env File Contents**

Your .env file should contain the following key-value pairs:
```
OPENAI_API_KEY='your_openai_api_key_here'
PINECONE_API_KEY='your_pinecone_api_key_here'
PINECONE_ENVIRONMENT_REGION='your_pinecone_region_here'
```
> Please ensure that your .env file is never committed to your version control system. Add .env to your .gitignore file to prevent accidental uploads of sensitive information.

## Setup

### Run locally with Docker

<details>
<summary> Dockerfile </summary>

```shell
# Base image selection
FROM python:3.11.7-bookworm

# Set working directory in container
WORKDIR /app

# Set up networking to container
EXPOSE 8501

# Copy local files to the container location
COPY . /app/

# Set up environment
# RUN mkdir /app/langchain-docs
RUN apt update && apt install -y wget
RUN pip install pipenv
# Download langchain documentation
RUN wget -r -A.html -P ./langchain-docs https://api.python.langchain.com/en/latest/index.html

# Set up dependencies for the documentation helper flask server
RUN pipenv --python /usr/local/bin/python
RUN pipenv install

# Upload langchain docs to Pinecone
RUN pipenv python setup_ingestion.py

# Container start command
CMD [ "pipenv", "run", "streamlit", "run", "app.py" ]
```
</details>

#### Script to build and run docker container
```shell
#!/bin/bash -x

# Builds the local image
docker build -t documentation-helper:0.1 .

# Start the container
docker run -d --name docs-h -p 8501:8501 docs-helper:0.1
```
![qfuQHf](https://testksj.oss-cn-beijing.aliyuncs.com/uPic/qfuQHf.png)

> 🥳 Now, go to http://localhost:8501/ to talk with your bot!
