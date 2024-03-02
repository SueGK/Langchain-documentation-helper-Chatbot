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

## Run locally with Docker

### Setup

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

1. Clone the repository:
```bash
git clone https://github.com/SueGK/documentation-helper.git
```
2. Navigate to the project directory:
```bash
cd documentation-helper
```
3. Run the Script to build and run docker container
```bash
python start-doc-helper.sh  
```
[start-doc-helper.sh](https://github.com/SueGK/documentation-helper/blob/local-docker/start-doc-helper.sh) contains:
```shell
#!/bin/bash -x

# Builds the local image
docker build -t documentation-helper:0.1 .

# Start the container
docker run -d --name docs-h -p 8501:8501 docs-helper:0.1
```
![qfuQHf](https://testksj.oss-cn-beijing.aliyuncs.com/uPic/qfuQHf.png)

> 🥳 Now, go to http://localhost:8501/ to talk with your bot!

## Deploy to streamlit cloud


<a href="https://suegk-documentation-helper-app-deploy-streamlit-cloud-fhbl90.streamlit.app/?embed_options=show_toolbar,light_theme,show_colored_line,show_padding,dark_theme">
    <img src="https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2FFemFarm%2FUsryQ3eMyk.png?alt=media&token=f8c1412d-6220-4d90-8900-883ee0c4e393" width="700">
</a>


🔥 **CLICK IMAGE TO START TALKING TO THE BOT, SET UP YOUR API AT API SETTING PAGES**





### Setup

1. Clone the repository:
```bash
git clone https://github.com/SueGK/documentation-helper.git
```
2. Navigate to the project directory:
```bash
cd documentation-helper
```

3. Change to deploy-streamlit-cloud branch
```bash
git checkout deploy-streamlit-cloud
```
4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Download LangChain Documentation
```bash
  mkdir langchain-docs
  wget -r -A.html -P langchain-docs  https://api.python.langchain.com/en/latest
```
6. Embed LangChain Official Documentation into Pinecone Index Using OpenAI's Embedding Model
```bash
python setup_ingestion.py
```
7. Start the server
```bash
streamlit run app.py
```
8. Deploy on streamlit cloud

## Debug Streamlit Applications in VSCode
To debug a Streamlit application, you need to create a launch configuration for Python:

Go to the Run and Debug view by clicking on the play icon with a bug on the sidebar or pressing Ctrl+Shift+D (Cmd+Shift+D on macOS).
Click on "create a launch.json file" link, then select the Python environment you're using for your Streamlit app.
Replace the content of the [launch.json](https://github.com/SueGK/documentation-helper/blob/deploy-streamlit-cloud/.vscode/launch.json) file with the following configuration:
```json
{
    "version": "0.2.0",
    "configurations": [
        
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            // use pipenv --venv to change the path
            "program": "PATH/TO/VENV/bin/streamlit",
            "console": "integratedTerminal",
            "justMyCode": true,
            "args": ["run","app.py"]
        }
    ]
}
```
> Make sure to change **"program": "PATH/TO/VENV/bin/streamlit"**

